# 상품 정보 서비스

## ProductService.java

### service

상품 정보의 CRUD 작업과 재고 관리를 처리하는 서비스 클래스입니다.

```java
package com.shoppingmall.service;

import com.shoppingmall.bean.Product;
import com.shoppingmall.dbio.ProductRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

/**
 * 상품 정보의 CRUD 작업과 재고 관리를 처리하는 서비스 클래스
 * 
 * @author shoppingmall
 * @version 1.0
 * @since 2024-03-19
 */
@Service
@RequiredArgsConstructor
public class ProductService {
    private final ProductRepository productRepository;

    /**
     * 새로운 상품을 생성합니다.
     * 
     * @param product 생성할 상품 정보
     * @return 생성된 상품 정보
     */
    @Transactional
    public Product createProduct(Product product) {
        return productRepository.save(product);
    }

    /**
     * ID로 상품을 조회합니다.
     * 
     * @param id 조회할 상품의 ID
     * @return 조회된 상품 정보 (Optional)
     */
    @Transactional(readOnly = true)
    public Optional<Product> getProductById(Long id) {
        return productRepository.findById(id);
    }

    /**
     * 모든 상품 목록을 조회합니다.
     * 
     * @return 전체 상품 목록
     */
    @Transactional(readOnly = true)
    public List<Product> getAllProducts() {
        return productRepository.findAll();
    }

    /**
     * 카테고리별 상품 목록을 조회합니다.
     * 
     * @param category 조회할 카테고리
     * @return 해당 카테고리의 상품 목록
     */
    @Transactional(readOnly = true)
    public List<Product> getProductsByCategory(String category) {
        return productRepository.findByCategory(category);
    }

    /**
     * 상품 정보를 수정합니다.
     * 
     * @param id 수정할 상품의 ID
     * @param productDetails 수정할 상품 정보
     * @return 수정된 상품 정보
     * @throws RuntimeException 상품이 존재하지 않는 경우
     */
    @Transactional
    public Product updateProduct(Long id, Product productDetails) {
        Product product = productRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Product not found"));
        
        product.setName(productDetails.getName());
        product.setDescription(productDetails.getDescription());
        product.setPrice(productDetails.getPrice());
        product.setStockQuantity(productDetails.getStockQuantity());
        product.setCategory(productDetails.getCategory());
        
        return productRepository.save(product);
    }

    /**
     * 상품을 삭제합니다.
     * 
     * @param id 삭제할 상품의 ID
     */
    @Transactional
    public void deleteProduct(Long id) {
        productRepository.deleteById(id);
    }

    /**
     * 상품의 재고를 수정합니다.
     * 
     * @param id 수정할 상품의 ID
     * @param quantity 변경할 재고 수량
     * @return 수정된 상품 정보
     * @throws RuntimeException 상품이 존재하지 않거나 재고가 부족한 경우
     */
    @Transactional
    public Product updateStock(Long id, int quantity) {
        Product product = productRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Product not found"));
        
        int newStock = product.getStockQuantity() + quantity;
        if (newStock < 0) {
            throw new RuntimeException("Insufficient stock");
        }
        
        product.setStockQuantity(newStock);
        return productRepository.save(product);
    }
} 