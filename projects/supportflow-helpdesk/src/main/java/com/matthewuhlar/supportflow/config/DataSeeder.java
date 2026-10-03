package com.matthewuhlar.supportflow.config;

import com.matthewuhlar.supportflow.model.*;
import com.matthewuhlar.supportflow.repository.*;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;

@Component
public class DataSeeder implements CommandLineRunner {
    private final UserRepository userRepository;
    private final TicketRepository ticketRepository;
    private final PasswordEncoder passwordEncoder;

    public DataSeeder(
        UserRepository userRepository,
        TicketRepository ticketRepository,
        PasswordEncoder passwordEncoder
    ) {
        this.userRepository = userRepository;
        this.ticketRepository = ticketRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @Override
    public void run(String... args) {
        if (userRepository.count() > 0) {
            return;
        }

        UserAccount admin = createUser(
            "Matthew Admin",
            "admin@example.com",
            "Admin123!",
            Role.ADMIN
        );

        UserAccount technician = createUser(
            "Demo Technician",
            "tech@example.com",
            "Tech123!",
            Role.TECHNICIAN
        );

        UserAccount employee = createUser(
            "Demo Employee",
            "employee@example.com",
            "Employee123!",
            Role.EMPLOYEE
        );

        Ticket firstTicket = new Ticket();
        firstTicket.setTitle("Warehouse scanner stopped formatting labels");
        firstTicket.setDescription(
            "The scanner started sending a different field format after a firmware update."
        );
        firstTicket.setPriority(TicketPriority.HIGH);
        firstTicket.setStatus(TicketStatus.IN_PROGRESS);
        firstTicket.setCreatedBy(employee);
        firstTicket.setAssignedTo(technician);

        Ticket secondTicket = new Ticket();
        secondTicket.setTitle("New employee needs application access");
        secondTicket.setDescription(
            "Set up the standard accounts and confirm access before the employee starts."
        );
        secondTicket.setPriority(TicketPriority.MEDIUM);
        secondTicket.setStatus(TicketStatus.OPEN);
        secondTicket.setCreatedBy(admin);

        ticketRepository.save(firstTicket);
        ticketRepository.save(secondTicket);
    }

    private UserAccount createUser(
        String name,
        String email,
        String password,
        Role role
    ) {
        UserAccount user = new UserAccount();
        user.setName(name);
        user.setEmail(email);
        user.setPasswordHash(passwordEncoder.encode(password));
        user.setRole(role);
        return userRepository.save(user);
    }
}
