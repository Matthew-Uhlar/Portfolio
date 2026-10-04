package com.matthewuhlar.supportflow.controller;

import com.matthewuhlar.supportflow.model.Role;
import com.matthewuhlar.supportflow.repository.UserRepository;
import java.util.List;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/users")
public class UserController {
    private final UserRepository userRepository;

    public UserController(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    /** People a ticket can be assigned to, for the assignment dropdown. */
    @GetMapping("/assignable")
    @PreAuthorize("hasAnyRole('TECHNICIAN', 'ADMIN')")
    public List<UserSummary> getAssignableUsers() {
        return userRepository.findByRoleInOrderByNameAsc(List.of(Role.TECHNICIAN, Role.ADMIN)).stream()
            .map(user -> new UserSummary(user.getId(), user.getName(), user.getRole().name()))
            .toList();
    }

    public record UserSummary(Long id, String name, String role) {}
}
