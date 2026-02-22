"""
Comprehensive logging configuration for the application
Provides structured logging with rotation and multiple handlers
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from datetime import datetime
import json
from typing import Any, Dict

# Log directory
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Add extra fields
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms
        
        return json.dumps(log_data, default=str)


class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output"""
    
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
    }
    RESET = '\033[0m'
    
    def format(self, record: logging.LogRecord) -> str:
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)


def setup_logging(
    app_name: str = "alkhayma",
    log_level: str = "INFO",
    enable_json: bool = False
) -> logging.Logger:
    """
    Setup comprehensive logging configuration
    
    Args:
        app_name: Application name for log files
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        enable_json: Enable JSON formatting for production
        
    Returns:
        Configured logger instance
    """
    
    # Create logger
    logger = logging.getLogger(app_name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Remove existing handlers
    logger.handlers = []
    
    # Formatters
    if enable_json:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    console_formatter = ColoredFormatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler - general logs
    file_handler = logging.handlers.RotatingFileHandler(
        LOG_DIR / f"{app_name}.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=10
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # File handler - errors only
    error_handler = logging.handlers.RotatingFileHandler(
        LOG_DIR / f"{app_name}_error.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=10
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)
    
    # File handler - access logs (for API requests)
    access_handler = logging.handlers.RotatingFileHandler(
        LOG_DIR / f"{app_name}_access.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=10
    )
    access_handler.setLevel(logging.INFO)
    access_handler.setFormatter(formatter)
    
    # Create access logger
    access_logger = logging.getLogger(f"{app_name}.access")
    access_logger.addHandler(access_handler)
    
    return logger


# Request logging context
class RequestContext:
    """Context manager for request logging"""
    
    def __init__(self, logger: logging.Logger, request_id: str, user_id: str = None):
        self.logger = logger
        self.request_id = request_id
        self.user_id = user_id
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.utcnow()
        extra = {"request_id": self.request_id}
        if self.user_id:
            extra["user_id"] = self.user_id
        self.logger.debug("Request started", extra=extra)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.utcnow() - self.start_time).total_seconds() * 1000
        extra = {
            "request_id": self.request_id,
            "duration_ms": round(duration, 2)
        }
        if self.user_id:
            extra["user_id"] = self.user_id
        
        if exc_type:
            self.logger.error(
                f"Request failed after {duration:.2f}ms",
                extra=extra,
                exc_info=(exc_type, exc_val, exc_tb)
            )
        else:
            self.logger.info(f"Request completed in {duration:.2f}ms", extra=extra)


def log_request(
    logger: logging.Logger,
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    user_id: str = None,
    ip_address: str = None
):
    """
    Log API request details
    
    Args:
        logger: Logger instance
        method: HTTP method
        path: Request path
        status_code: HTTP status code
        duration_ms: Request duration in milliseconds
        user_id: Optional user ID
        ip_address: Optional client IP
    """
    log_data = {
        "event": "api_request",
        "method": method,
        "path": path,
        "status_code": status_code,
        "duration_ms": round(duration_ms, 2),
    }
    
    if user_id:
        log_data["user_id"] = user_id
    if ip_address:
        log_data["ip_address"] = ip_address
    
    if status_code >= 500:
        logger.error(json.dumps(log_data))
    elif status_code >= 400:
        logger.warning(json.dumps(log_data))
    else:
        logger.info(json.dumps(log_data))


def log_security_event(
    logger: logging.Logger,
    event_type: str,
    details: Dict[str, Any],
    severity: str = "warning"
):
    """
    Log security-related events
    
    Args:
        logger: Logger instance
        event_type: Type of security event (e.g., 'rate_limit_exceeded', 'suspicious_activity')
        details: Event details
        severity: Log level (debug, info, warning, error, critical)
    """
    log_data = {
        "event": "security",
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        **details
    }
    
    log_func = getattr(logger, severity.lower(), logger.warning)
    log_func(json.dumps(log_data))
