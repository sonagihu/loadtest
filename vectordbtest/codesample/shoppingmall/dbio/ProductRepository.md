# 상품 정보 데이터베이스 접근

## ProductRepository.java

### dbio

상품 정보의 데이터베이스 접근을 담당하는 Repository 인터페이스입니다.

```java
package com.shoppingmall.dbio;

import com.shoppingmall.bean.Product;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

/**
 * 상품 정보의 데이터베이스 접근을 담당하는 Repository 인터페이스
 * 
 * @author shoppingmall
 * @version 1.0
 * @since 2024-03-19
 */
@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {
    /**
     * 카테고리별 상품 목록을 조회합니다.
     * 
     * @param category 조회할 상품의 카테고리
     * @return 해당 카테고리의 상품 목록
     */
    List<Product> findByCategory(String category);
} 