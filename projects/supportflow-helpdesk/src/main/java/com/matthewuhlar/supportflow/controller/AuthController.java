package com.matthewuhlar.supportflow.controller;

import com.matthewuhlar.supportflow.dto.AuthDtos.LoginRequest;
import com.matthewuhlar.supportflow.dto.AuthDtos.LoginResponse;
import com.matthewuhlar.supportflow.repository.UserRepository;
import com.matthewuhlar.supportflow.security.JwtService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;

    public AuthController(
        UserRepository userRepository,
        PasswordEncoder passwordEncoder,
        JwtService jwtService
    ) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.jwtService = jwtService;
    }

    @PostMapping("/login")
    public ResponseEntity<?> login(@Valid @RequestBody LoginRequest request) {
        var user = userRepository.findByEmailIgnoreCase(request.email())
            .orElse(null);

        if (user == null || !passwordEncoder.matches(request.password(), user.getPasswordHash())) {
            return ResponseEntity.status(401)
                .body(new ErrorResponse("The email or password was not correct."));
        }

        return ResponseEntity.ok(
            new LoginResponse(
                jwtService.createToken(user),
                user.getName(),
                user.getRole().name()
            )
        );
    }

    private record ErrorResponse(String message) {}
}
