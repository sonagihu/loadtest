다음은 요구사항에 맞춘 `UserService` 클래스의 구현입니다:

```java
import java.util.HashMap;
import java.util.Map;

public class UserService {

    private Map<Long, User> users = new HashMap<>();

    public void createUser(User user) throws IllegalArgumentException {
        if (user == null || user.getName() == null || user.getEmail() == null) {
            throw new IllegalArgumentException("User must have a name and email.");
        }
        Long id = generateUserId();
        user.setId(id);
        users.put(id, user);
    }

    public User getUser(Long id) throws NullPointerException, IllegalArgumentException {
        if (id == null) {
            throw new NullPointerException("ID cannot be null");
        }
        User user = users.get(id);
        if (user == null) {
            throw new IllegalArgumentException("User with ID " + id + " does not exist.");
        }
        return user;
    }

    public void updateUser(Long id, String name, String email) throws NullPointerException, IllegalArgumentException {
        if (id == null || name == null || email == null) {
            throw new NullPointerException("ID, Name and Email cannot be null");
        }
        User user = users.get(id);
        if (user == null) {
            throw new IllegalArgumentException("User with ID " + id + " does not exist.");
        }
        user.setName(name);
        user.setEmail(email);
    }

    public void deleteUser(Long id) throws NullPointerException, IllegalArgumentException {
        if (id == null) {
            throw new NullPointerException("ID cannot be null");
        }
        User user = users.remove(id);
        if (user == null) {
            throw new IllegalArgumentException("User with ID " + id + " does not exist.");
        }
    }

    private Long generateUserId() {
        // 이 부분은 실제 시스템에서는 데이터베이스로부터 유니크한 ID를 생성하는 로직으로 대체되어야 합니다.
        return users.size() + 1L;
    }
}

class User {
    private Long id;
    private String name;
    private String email;
    private long createdAt;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public long getCreatedAt() {
        return createdAt;
    }

    public User(Long id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.createdAt = System.currentTimeMillis();
    }
}
```

이 클래스는 사용자 정보를 관리하기 위한 간단한 서비스 구현을 제공합니다. `User` 클래스는 사용자의 기본 정보를 저장하고 있으며, `UserService` 클래스에서는 해당 정보를 CRUD 연산을 통해 처리합니다.

- `createUser`: 새로운 사용자를 생성하고 ID를 할당합니다.
- `getUser`: 주어진 ID에 해당하는 사용자 정보를 반환합니다.
- `updateUser`: 사용자 정보를 업데이트 합니다.
- `deleteUser`: 주어진 ID의 사용자를 삭제합니다.

각 메소드는 예외 처리를 포함하여 잘못된 입력이나 없는 ID와 같은 상황에서 적절한 오류 메시지를 제공합니다.