# 주문 상품 정보 관리

## OrderItem.java

### bean

주문에 포함된 개별 상품의 수량과 가격 정보를 관리하는 엔티티 클래스입니다.

```java
package com.shoppingmall.bean;

import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;

/**
 * 주문에 포함된 개별 상품의 수량과 가격 정보를 관리하는 엔티티 클래스
 * 
 * @author shoppingmall
 * @version 1.0
 * @since 2024-03-19
 */
@Data
@Entity
@Table(name = "order_items")
public class OrderItem {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id", nullable = false)
    private Order order;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "product_id", nullable = false)
    private Product product;

    @Column(nullable = false)
    private Integer quantity;

    @Column(name = "unit_price", nullable = false)
    private BigDecimal unitPrice;

    @Column(name = "total_price", nullable = false)
    private BigDecimal totalPrice;
} 