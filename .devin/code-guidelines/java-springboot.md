## JAVA / SPRING BOOT GUIDELINES

> Placeholder. Expand with project-specific rules; review-mode enforces these alongside core-standards.md.

### Class Design
- Domain-driven design (DDD) for API and class naming
- Small classes (max 7 fields, 3-5 public methods)
- Prefer value objects over primitives

### Dependency Injection
- Constructor injection without @Autowired
- No field injection
- No Lombok

### Layering
- Proper transactional boundaries (@Service layer)
- Avoid JPA entities in web layer; use Request/Response DTOs

### Configuration
- Use typed configuration with @ConfigurationProperties
