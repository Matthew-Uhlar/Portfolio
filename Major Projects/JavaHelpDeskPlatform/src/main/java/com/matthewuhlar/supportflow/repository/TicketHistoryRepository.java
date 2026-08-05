package com.matthewuhlar.supportflow.repository;

import com.matthewuhlar.supportflow.model.TicketHistory;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TicketHistoryRepository extends JpaRepository<TicketHistory, Long> {
}
