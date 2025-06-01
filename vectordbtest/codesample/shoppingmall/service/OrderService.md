# 주문 관리 서비스

## OrderService.java

### service

주문 생성, 조회, 상태 관리, 취소 및 재고 관리를 처리하는 서비스 클래스입니다.

```java
package com.shoppingmall.service;

import com.shoppingmall.bean.*;
import com.shoppingmall.dbio.OrderRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

/**
 * 주문 생성, 조회, 상태 관리, 취소 및 재고 관리를 처리하는 서비스 클래스
 * 
 * @author shoppingmall
 * @version 1.0
 * @since 2024-03-19
 */
@Service
@RequiredArgsConstructor
public class OrderService {
    private final OrderRepository orderRepository;
    private final ProductService productService;
    private final CustomerService customerService;

    /**
     * 새로운 주문을 생성합니다.
     * 
     * @param customerId 주문할 고객의 ID
     * @param orderItems 주문할 상품 목록
     * @return 생성된 주문 정보
     * @throws RuntimeException 고객이 존재하지 않거나 상품이 존재하지 않거나 재고가 부족한 경우
     */
    @Transactional
    public Order createOrder(Long customerId, List<OrderItem> orderItems) {
        Customer customer = customerService.getCustomerById(customerId)
                .orElseThrow(() -> new RuntimeException("Customer not found"));

        Order order = new Order();
        order.setCustomer(customer);
        order.setOrderItems(orderItems);
        order.setStatus(Order.OrderStatus.PENDING);

        // 재고 확인 및 업데이트
        for (OrderItem item : orderItems) {
            Product product = productService.getProductById(item.getProduct().getId())
                    .orElseThrow(() -> new RuntimeException("Product not found"));
            
            if (product.getStockQuantity() < item.getQuantity()) {
                throw new RuntimeException("Insufficient stock for product: " + product.getName());
            }
            
            productService.updateStock(product.getId(), -item.getQuantity());
            item.setOrder(order);
            item.setUnitPrice(product.getPrice());
            item.setTotalPrice(product.getPrice() * item.getQuantity());
        }

        // 총 주문 금액 계산
        double totalAmount = orderItems.stream()
                .mapToDouble(OrderItem::getTotalPrice)
                .sum();
        order.setTotalAmount(totalAmount);

        return orderRepository.save(order);
    }

    /**
     * ID로 주문을 조회합니다.
     * 
     * @param id 조회할 주문의 ID
     * @return 조회된 주문 정보 (Optional)
     */
    @Transactional(readOnly = true)
    public Optional<Order> getOrderById(Long id) {
        return orderRepository.findById(id);
    }

    /**
     * 고객의 주문 목록을 조회합니다.
     * 
     * @param customerId 조회할 고객의 ID
     * @return 해당 고객의 주문 목록
     */
    @Transactional(readOnly = true)
    public List<Order> getOrdersByCustomerId(Long customerId) {
        return orderRepository.findByCustomerId(customerId);
    }

    /**
     * 주문 상태를 수정합니다.
     * 
     * @param id 수정할 주문의 ID
     * @param status 변경할 주문 상태
     * @return 수정된 주문 정보
     * @throws RuntimeException 주문이 존재하지 않는 경우
     */
    @Transactional
    public Order updateOrderStatus(Long id, Order.OrderStatus status) {
        Order order = orderRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Order not found"));
        
        order.setStatus(status);
        return orderRepository.save(order);
    }

    /**
     * 주문을 취소합니다.
     * 
     * @param id 취소할 주문의 ID
     * @throws RuntimeException 주문이 존재하지 않거나 취소할 수 없는 상태인 경우
     */
    @Transactional
    public void cancelOrder(Long id) {
        Order order = orderRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Order not found"));
        
        if (order.getStatus() != Order.OrderStatus.PENDING) {
            throw new RuntimeException("Cannot cancel order in status: " + order.getStatus());
        }

        // 재고 복구
        for (OrderItem item : order.getOrderItems()) {
            productService.updateStock(item.getProduct().getId(), item.getQuantity());
        }

        order.setStatus(Order.OrderStatus.CANCELLED);
        orderRepository.save(order);
    }
} 