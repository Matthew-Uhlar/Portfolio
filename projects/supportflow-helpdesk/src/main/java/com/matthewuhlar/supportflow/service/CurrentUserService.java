package com.matthewuhlar.supportflow.service;

import com.matthewuhlar.supportflow.model.UserAccount;
import com.matthewuhlar.supportflow.repository.UserRepository;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

@Service
public class CurrentUserService {
    private final UserRepository userRepository;

    public CurrentUserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public UserAccount getCurrentUser() {
        String email = SecurityContextHolder.getContext().getAuthentication().getName();

        return userRepository.findByEmailIgnoreCase(email)
            .orElseThrow(() -> new IllegalStateException("The signed-in user could not be found."));
    }
}
