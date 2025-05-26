다음은 주어진 요구사항에 맞춰 작성된 `UserService` 클래스입니다.

```java
import java.util.HashMap;
import java.util.Map;

public class UserService {

    private Map<Integer, User> users = new HashMap<>();

    // 사용자 생성 메소드
    public void createUser(int id, String name, String email) {
        if (users.containsKey(id)) {
            throw new IllegalArgumentException("User with the given ID already exists.");
        }
        User newUser = new User(id, name, email);
        users.put(id, newUser);
        System.out.println("User created successfully: " + newUser);
    }

    // 사용자 조회 메소드
    public User getUser(int id) {
        if (!users.containsKey(id)) {
            throw new IllegalArgumentException("User with the given ID does not exist.");
        }
        return users.get(id);
    }

    // 사용자 정보 수정 메소드
    public void updateUser(int id, String name, String email) {
        if (!users.containsKey(id)) {
            throw new IllegalArgumentException("User with the given ID does not exist.");
        }
        User user = users.get(id);
        user.setName(name);
        user.setEmail(email);
        System.out.println("User updated successfully: " + user);
    }

    // 사용자 삭제 메소드
    public void deleteUser(int id) {
        if (!users.containsKey(id)) {
            throw new IllegalArgumentException("User with the given ID does not exist.");
        }
        users.remove(id);
        System.out.println("User deleted successfully with ID: " + id);
    }

    private static class User {
        int id;
        String name;
        String email;
        long createdAt;

        public User(int id, String name, String email) {
            this.id = id;
            this.name = name;
            this.email = email;
            this.createdAt = System.currentTimeMillis();
        }

        @Override
        public String toString() {
            return "User{" +
                    "id=" + id +
                    ", name='" + name + '\'' +
                    ", email='" + email + '\'' +
                    ", createdAt=" + createdAt +
                    '}';
        }
    }
}
```

이 클래스는 다음과 같은 기능을 제공합니다:

1. `createUser` - 사용자를 생성하고, 이미 해당 ID로 등록된 사용자가 있는 경우 예외를 던집니다.
2. `getUser` - 사용자 정보를 반환하며, 없는 사용자의 경우 예외를 던집니다.
3. `updateUser` - 기존 사용자의 정보를 수정하고, 없는 사용자의 경우 예외를 던집니다.
4. `deleteUser` - 사용자를 삭제하고, 없는 사용자의 경우 예외를 던집니다.

사용자 정보는 `id`, `name`, `email`, 그리고 `createdAt` 필드로 구성되며, `createdAt`은 생성 시점의 시간을 기록합니다.