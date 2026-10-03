package com.matthewuhlar.supportflow.repository;

import com.matthewuhlar.supportflow.model.TicketComment;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TicketCommentRepository extends JpaRepository<TicketComment, Long> {
}
