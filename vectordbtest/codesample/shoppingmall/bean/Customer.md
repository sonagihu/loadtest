# 고객 정보 관리

## Customer.java

### bean

고객의 기본 정보와 생성/수정 시간을 관리하는 엔티티 클래스입니다.

```java
package com.shoppingmall.bean;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

/**
 * 고객의 기본 정보와 생성/수정 시간을 관리하는 엔티티 클래스
 * 
 * @author shoppingmall
 * @version 1.0
 * @since 2024-03-19
 */
@Data
@Entity
@Table(name = "customers")
public class Customer {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String password;

    @Column(name = "phone_number")
    private String phoneNumber;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
} 