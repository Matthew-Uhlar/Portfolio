package com.matthewuhlar.supportflow.controller;

import com.matthewuhlar.supportflow.model.TicketPriority;
import com.matthewuhlar.supportflow.model.TicketStatus;
import com.matthewuhlar.supportflow.repository.TicketRepository;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/dashboard")
public class DashboardController {
    private final TicketRepository ticketRepository;

    public DashboardController(TicketRepository ticketRepository) {
        this.ticketRepository = ticketRepository;
    }

    @GetMapping
    public Map<String, Long> getDashboard() {
        var tickets = ticketRepository.findAll();

        return Map.of(
            "totalTickets", (long) tickets.size(),
            "openTickets", tickets.stream()
                .filter(ticket -> ticket.getStatus() != TicketStatus.CLOSED)
                .count(),
            "criticalTickets", tickets.stream()
                .filter(ticket -> ticket.getPriority() == TicketPriority.CRITICAL)
                .filter(ticket -> ticket.getStatus() != TicketStatus.CLOSED)
                .count(),
            "resolvedTickets", tickets.stream()
                .filter(ticket -> ticket.getStatus() == TicketStatus.RESOLVED)
                .count()
        );
    }
}
