# 주문 관리 API

## OrderController.java

### controller

주문 생성, 조회, 상태 관리, 취소를 처리하는 REST API 컨트롤러입니다.

```java
package com.shoppingmall.controller;

import com.shoppingmall.bean.Order;
import com.shoppingmall.bean.OrderItem;
import com.shoppingmall.service.OrderService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 주문 생성, 조회, 상태 관리, 취소를 처리하는 REST API 컨트롤러
 * 
 * @author shoppingmall
 * @version 1.0
 * @since 2024-03-19
 */
@RestController
@RequestMapping("/api/orders")
@RequiredArgsConstructor
public class OrderController {
    private final OrderService orderService;

    /**
     * 새로운 주문을 생성합니다.
     * 
     * @param customerId 주문할 고객의 ID
     * @param orderItems 주문할 상품 목록
     * @return 생성된 주문 정보
     */
    @PostMapping("/customer/{customerId}")
    public ResponseEntity<Order> createOrder(
            @PathVariable Long customerId,
            @RequestBody List<OrderItem> orderItems) {
        return ResponseEntity.ok(orderService.createOrder(customerId, orderItems));
    }

    /**
     * ID로 주문을 조회합니다.
     * 
     * @param id 조회할 주문의 ID
     * @return 조회된 주문 정보
     */
    @GetMapping("/{id}")
    public ResponseEntity<Order> getOrder(@PathVariable Long id) {
        return orderService.getOrderById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * 고객의 주문 목록을 조회합니다.
     * 
     * @param customerId 조회할 고객의 ID
     * @return 해당 고객의 주문 목록
     */
    @GetMapping("/customer/{customerId}")
    public ResponseEntity<List<Order>> getOrdersByCustomer(@PathVariable Long customerId) {
        return ResponseEntity.ok(orderService.getOrdersByCustomerId(customerId));
    }

    /**
     * 주문 상태를 수정합니다.
     * 
     * @param id 수정할 주문의 ID
     * @param status 변경할 주문 상태
     * @return 수정된 주문 정보
     */
    @PutMapping("/{id}/status")
    public ResponseEntity<Order> updateOrderStatus(
            @PathVariable Long id,
            @RequestParam Order.OrderStatus status) {
        return ResponseEntity.ok(orderService.updateOrderStatus(id, status));
    }

    /**
     * 주문을 취소합니다.
     * 
     * @param id 취소할 주문의 ID
     * @return 성공 응답
     */
    @PostMapping("/{id}/cancel")
    public ResponseEntity<Void> cancelOrder(@PathVariable Long id) {
        orderService.cancelOrder(id);
        return ResponseEntity.ok().build();
    }
} 