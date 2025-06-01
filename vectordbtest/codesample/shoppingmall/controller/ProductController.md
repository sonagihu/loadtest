# 상품 정보 API

## ProductController.java

### controller

상품 정보의 CRUD 작업과 재고 관리를 처리하는 REST API 컨트롤러입니다.

```java
package com.shoppingmall.controller;

import com.shoppingmall.bean.Product;
import com.shoppingmall.service.ProductService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 상품 정보의 CRUD 작업과 재고 관리를 처리하는 REST API 컨트롤러
 * 
 * @author shoppingmall
 * @version 1.0
 * @since 2024-03-19
 */
@RestController
@RequestMapping("/api/products")
@RequiredArgsConstructor
public class ProductController {
    private final ProductService productService;

    /**
     * 새로운 상품을 생성합니다.
     * 
     * @param product 생성할 상품 정보
     * @return 생성된 상품 정보
     */
    @PostMapping
    public ResponseEntity<Product> createProduct(@RequestBody Product product) {
        return ResponseEntity.ok(productService.createProduct(product));
    }

    /**
     * ID로 상품을 조회합니다.
     * 
     * @param id 조회할 상품의 ID
     * @return 조회된 상품 정보
     */
    @GetMapping("/{id}")
    public ResponseEntity<Product> getProduct(@PathVariable Long id) {
        return productService.getProductById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * 모든 상품 목록을 조회합니다.
     * 
     * @return 전체 상품 목록
     */
    @GetMapping
    public ResponseEntity<List<Product>> getAllProducts() {
        return ResponseEntity.ok(productService.getAllProducts());
    }

    /**
     * 카테고리별 상품 목록을 조회합니다.
     * 
     * @param category 조회할 카테고리
     * @return 해당 카테고리의 상품 목록
     */
    @GetMapping("/category/{category}")
    public ResponseEntity<List<Product>> getProductsByCategory(@PathVariable String category) {
        return ResponseEntity.ok(productService.getProductsByCategory(category));
    }

    /**
     * 상품 정보를 수정합니다.
     * 
     * @param id 수정할 상품의 ID
     * @param product 수정할 상품 정보
     * @return 수정된 상품 정보
     */
    @PutMapping("/{id}")
    public ResponseEntity<Product> updateProduct(@PathVariable Long id, @RequestBody Product product) {
        return ResponseEntity.ok(productService.updateProduct(id, product));
    }

    /**
     * 상품을 삭제합니다.
     * 
     * @param id 삭제할 상품의 ID
     * @return 성공 응답
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteProduct(@PathVariable Long id) {
        productService.deleteProduct(id);
        return ResponseEntity.ok().build();
    }

    /**
     * 상품의 재고를 수정합니다.
     * 
     * @param id 수정할 상품의 ID
     * @param quantity 변경할 재고 수량
     * @return 수정된 상품 정보
     */
    @PutMapping("/{id}/stock")
    public ResponseEntity<Product> updateStock(@PathVariable Long id, @RequestParam int quantity) {
        return ResponseEntity.ok(productService.updateStock(id, quantity));
    }
} 