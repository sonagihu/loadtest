# 고객 정보 API

## CustomerController.java

### controller

고객 정보의 CRUD 작업을 처리하는 REST API 컨트롤러입니다.

```java
package com.shoppingmall.controller;

import com.shoppingmall.bean.Customer;
import com.shoppingmall.service.CustomerService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * 고객 정보의 CRUD 작업을 처리하는 REST API 컨트롤러
 * 
 * @author shoppingmall
 * @version 1.0
 * @since 2024-03-19
 */
@RestController
@RequestMapping("/api/customers")
@RequiredArgsConstructor
public class CustomerController {
    private final CustomerService customerService;

    /**
     * 새로운 고객을 생성합니다.
     * 
     * @param customer 생성할 고객 정보
     * @return 생성된 고객 정보
     */
    @PostMapping
    public ResponseEntity<Customer> createCustomer(@RequestBody Customer customer) {
        return ResponseEntity.ok(customerService.createCustomer(customer));
    }

    /**
     * ID로 고객을 조회합니다.
     * 
     * @param id 조회할 고객의 ID
     * @return 조회된 고객 정보
     */
    @GetMapping("/{id}")
    public ResponseEntity<Customer> getCustomer(@PathVariable Long id) {
        return customerService.getCustomerById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    /**
     * 모든 고객 목록을 조회합니다.
     * 
     * @return 전체 고객 목록
     */
    @GetMapping
    public ResponseEntity<List<Customer>> getAllCustomers() {
        return ResponseEntity.ok(customerService.getAllCustomers());
    }

    /**
     * 고객 정보를 수정합니다.
     * 
     * @param id 수정할 고객의 ID
     * @param customer 수정할 고객 정보
     * @return 수정된 고객 정보
     */
    @PutMapping("/{id}")
    public ResponseEntity<Customer> updateCustomer(@PathVariable Long id, @RequestBody Customer customer) {
        return ResponseEntity.ok(customerService.updateCustomer(id, customer));
    }

    /**
     * 고객을 삭제합니다.
     * 
     * @param id 삭제할 고객의 ID
     * @return 성공 응답
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteCustomer(@PathVariable Long id) {
        customerService.deleteCustomer(id);
        return ResponseEntity.ok().build();
    }

    /**
     * 이메일로 고객을 조회합니다.
     * 
     * @param email 조회할 고객의 이메일
     * @return 조회된 고객 정보
     */
    @GetMapping("/email/{email}")
    public ResponseEntity<Customer> getCustomerByEmail(@PathVariable String email) {
        return customerService.getCustomerByEmail(email)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
} 