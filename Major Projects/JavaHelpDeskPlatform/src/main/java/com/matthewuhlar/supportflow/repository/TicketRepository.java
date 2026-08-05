package com.matthewuhlar.supportflow.repository;

import com.matthewuhlar.supportflow.model.*;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface TicketRepository extends JpaRepository<Ticket, Long> {
    List<Ticket> findByStatusOrderByCreatedAtDesc(TicketStatus status);
    List<Ticket> findByPriorityOrderByCreatedAtDesc(TicketPriority priority);
    List<Ticket> findByCreatedByIdOrderByCreatedAtDesc(Long userId);
    List<Ticket> findByAssignedToIdOrderByCreatedAtDesc(Long userId);
}
