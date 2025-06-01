# 고객 정보 서비스

## CustomerService.java

### service

고객 정보의 생성, 조회, 수정, 삭제를 처리하는 서비스 클래스입니다.

```java
package com.shoppingmall.service;

import com.shoppingmall.bean.Customer;
import com.shoppingmall.dbio.CustomerRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

/**
 * 고객 정보의 생성, 조회, 수정, 삭제를 처리하는 서비스 클래스
 * 
 * @author shoppingmall
 * @version 1.0
 * @since 2024-03-19
 */
@Service
@RequiredArgsConstructor
public class CustomerService {
    private final CustomerRepository customerRepository;

    /**
     * 새로운 고객을 생성합니다.
     * 
     * @param customer 생성할 고객 정보
     * @return 생성된 고객 정보
     */
    @Transactional
    public Customer createCustomer(Customer customer) {
        return customerRepository.save(customer);
    }

    /**
     * ID로 고객을 조회합니다.
     * 
     * @param id 조회할 고객의 ID
     * @return 조회된 고객 정보 (Optional)
     */
    @Transactional(readOnly = true)
    public Optional<Customer> getCustomerById(Long id) {
        return customerRepository.findById(id);
    }

    /**
     * 모든 고객 목록을 조회합니다.
     * 
     * @return 전체 고객 목록
     */
    @Transactional(readOnly = true)
    public List<Customer> getAllCustomers() {
        return customerRepository.findAll();
    }

    /**
     * 고객 정보를 수정합니다.
     * 
     * @param id 수정할 고객의 ID
     * @param customerDetails 수정할 고객 정보
     * @return 수정된 고객 정보
     * @throws RuntimeException 고객이 존재하지 않는 경우
     */
    @Transactional
    public Customer updateCustomer(Long id, Customer customerDetails) {
        Customer customer = customerRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Customer not found"));
        
        customer.setName(customerDetails.getName());
        customer.setEmail(customerDetails.getEmail());
        customer.setPhoneNumber(customerDetails.getPhoneNumber());
        
        return customerRepository.save(customer);
    }

    /**
     * 고객을 삭제합니다.
     * 
     * @param id 삭제할 고객의 ID
     */
    @Transactional
    public void deleteCustomer(Long id) {
        customerRepository.deleteById(id);
    }

    /**
     * 이메일로 고객을 조회합니다.
     * 
     * @param email 조회할 고객의 이메일
     * @return 조회된 고객 정보 (Optional)
     */
    @Transactional(readOnly = true)
    public Optional<Customer> getCustomerByEmail(String email) {
        return customerRepository.findByEmail(email);
    }
} 