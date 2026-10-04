package com.matthewuhlar.supportflow.repository;

import com.matthewuhlar.supportflow.model.Role;
import com.matthewuhlar.supportflow.model.UserAccount;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Collection;
import java.util.List;
import java.util.Optional;

public interface UserRepository extends JpaRepository<UserAccount, Long> {
    Optional<UserAccount> findByEmailIgnoreCase(String email);
    List<UserAccount> findByRoleInOrderByNameAsc(Collection<Role> roles);
}
