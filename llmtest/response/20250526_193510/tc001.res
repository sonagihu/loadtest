아래는 요구사항에 맞춘 `UserService` 클래스의 예제 코드입니다.

```java
import java.util.HashMap;
import java.util.Map;

public class UserService {

    // User 정보 저장을 위한 Map (key: id, value: User)
    private final Map<Integer, User> users = new HashMap<>();

    public void createUser(String name, String email) throws Exception {
        if (!users.containsKey(name.hashCode())) {  // 중복 ID 체크
            int userId = generateUserId();
            User newUser = new User(userId, name, email);
            users.put(newUser.getId(), newUser);
        } else {
            throw new Exception("User with this name already exists.");
        }
    }

    public User getUser(String name) throws Exception {
        Integer userId = name.hashCode();
        if (users.containsKey(userId)) {
            return users.get(userId);
        } else {
            throw new Exception("User not found.");
        }
    }

    public void updateUser(int id, String newName, String newEmail) throws Exception {
        if (users.containsKey(id)) {
            User user = users.get(id);
            user.setName(newName);
            user.setEmail(newEmail);
            // createdAt은 수정되지 않으므로 업데이트 X
        } else {
            throw new Exception("User not found.");
        }
    }

    public void deleteUser(int id) throws Exception {
        if (users.containsKey(id)) {
            users.remove(id);
        } else {
            throw new Exception("User not found.");
        }
    }

    // ID 생성 메소드
    private int generateUserId() {
        return (int) (Math.random() * 10000);  // 임시로 사용되는 ID 생성, 실제 상황에서는 다른 로직이 필요할 수 있습니다.
    }

    public static class User {
        private final int id;
        private String name;
        private String email;
        private final long createdAt;

        public User(int id, String name, String email) {
            this.id = id;
            this.name = name;
            this.email = email;
            this.createdAt = System.currentTimeMillis();
        }

        public int getId() {
            return id;
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
    }
}
```

이 코드는 `UserService` 클래스를 정의합니다. 이 클래스는 사용자 정보를 관리하며 다음과 같은 기능을 제공합니다:

1. `createUser`: 새로운 사용자를 생성하고, 동일한 이름으로 이미 존재하는 사용자가 없는지 확인합니다.
2. `getUser`: 주어진 이름에 해당하는 사용자를 반환합니다.
3. `updateUser`: 사용자 정보를 업데이트합니다.
4. `deleteUser`: 사용자를 삭제합니다.

각 메소드는 예외 처리를 수행하며, 필요한 경우 관련 예외(`Exception`)를 던집니다. 또한, `User` 클래스 내부에 포함되어 사용자 정보를 저장하고 관리합니다.