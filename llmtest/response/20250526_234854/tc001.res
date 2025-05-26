이 요구사항에 따라 `UserService` 클래스를 작성해보겠습니다. 이 클래스는 사용자를 관리하는 기능을 가지고 있으며, 각 메소드에서 예외 처리도 함께 구현하였습니다.

```java
import java.util.HashMap;
import java.util.Map;

public class UserService {
    
    // 사용자 정보를 저장할 맵
    private Map<Integer, User> users = new HashMap<>();

    /**
     * 사용자를 생성합니다.
     * @param id 사용자의 고유 식별자
     * @param name 사용자의 이름
     * @param email 사용자의 이메일 주소
     */
    public void createUser(int id, String name, String email) {
        if (users.containsKey(id)) {
            throw new IllegalArgumentException("User already exists with ID: " + id);
        }
        
        User newUser = new User(id, name, email);
        users.put(id, newUser);
        System.out.println("User created successfully.");
    }

    /**
     * 사용자를 조회합니다.
     * @param id 사용자의 고유 식별자
     * @return 사용자 정보
     */
    public User getUser(int id) {
        if (!users.containsKey(id)) {
            throw new IllegalArgumentException("User with ID " + id + " does not exist.");
        }
        
        return users.get(id);
    }

    /**
     * 사용자의 정보를 수정합니다.
     * @param id 사용자의 고유 식별자
     * @param name 수정할 사용자의 이름
     * @param email 수정할 사용자의 이메일 주소
     */
    public void updateUser(int id, String name, String email) {
        if (!users.containsKey(id)) {
            throw new IllegalArgumentException("User with ID " + id + " does not exist.");
        }
        
        User user = users.get(id);
        user.setName(name);
        user.setEmail(email);
        System.out.println("User information updated successfully.");
    }

    /**
     * 사용자를 삭제합니다.
     * @param id 사용자의 고유 식별자
     */
    public void deleteUser(int id) {
        if (!users.containsKey(id)) {
            throw new IllegalArgumentException("User with ID " + id + " does not exist.");
        }
        
        users.remove(id);
        System.out.println("User deleted successfully.");
    }

    // 사용자 클래스 정의
    private static class User {
        private int id;
        private String name;
        private String email;
        private java.util.Date createdAt;

        public User(int id, String name, String email) {
            this.id = id;
            this.name = name;
            this.email = email;
            this.createdAt = new java.util.Date();
        }

        public int getId() {
            return id;
        }

        public void setId(int id) {
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
    }
}
```

위의 코드는 `UserService` 클래스를 정의하며, 각 기능별 메소드와 예외 처리를 포함하고 있습니다. 또한, 사용자 정보를 저장하기 위한 내부 클래스 `User`도 함께 구현하였습니다.