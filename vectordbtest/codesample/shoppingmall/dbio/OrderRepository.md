# 주문 정보 데이터베이스 접근

## OrderRepository.java

### dbio

주문 정보의 데이터베이스 접근을 담당하는 Repository 인터페이스입니다.

```java
package com.shoppingmall.dbio;

import com.shoppingmall.bean.Order;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * 주문 정보의 데이터베이스 접근을 담당하는 Repository 인터페이스
 * 
 * @author shoppingmall
 * @version 1.0
 * @since 2024-03-19
 */
@Repository
public interface OrderRepository extends JpaRepository<Order, Long> {
    /**
     * 고객 ID로 주문 목록을 조회합니다.
     * 
     * @param customerId 조회할 고객의 ID
     * @return 해당 고객의 주문 목록
     */
    List<Order> findByCustomerId(Long customerId);
} 