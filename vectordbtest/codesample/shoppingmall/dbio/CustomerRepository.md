# 고객 정보 데이터베이스 접근

## CustomerRepository.java

### dbio

고객 정보의 데이터베이스 접근을 담당하는 Repository 인터페이스입니다.

```java
package com.shoppingmall.dbio;

import com.shoppingmall.bean.Customer;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

/**
 * 고객 정보의 데이터베이스 접근을 담당하는 Repository 인터페이스
 * 
 * @author shoppingmall
 * @version 1.0
 * @since 2024-03-19
 */
@Repository
public interface CustomerRepository extends JpaRepository<Customer, Long> {
    /**
     * 이메일 주소로 고객을 조회합니다.
     * 
     * @param email 조회할 고객의 이메일 주소
     * @return 조회된 고객 정보 (Optional)
     */
    Optional<Customer> findByEmail(String email);
} 