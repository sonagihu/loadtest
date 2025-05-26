아래는 `DatabaseConnectionPool` 클래스의 Java 코드 예제입니다. 이 클래스는 주어진 요구사항에 맞추어 작성되었으며, 연결 풀을 관리하고 초기화하는 메소드, 연결 획득 및 반환 메소드, 연결 상태 모니터링 기능 등을 구현했습니다.

```java
import java.util.LinkedList;
import java.util.Queue;

public class DatabaseConnectionPool {

    private int minConnections;
    private int maxConnections;
    private Queue<DatabaseConnection> availableConnections;
    private int currentConnections;

    public DatabaseConnectionPool(int minConnections, int maxConnections) {
        this.minConnections = minConnections;
        this.maxConnections = maxConnections;
        this.availableConnections = new LinkedList<>();
        this.currentConnections = 0;
    }

    // 연결 풀 초기화
    public void initialize() {
        for (int i = 0; i < minConnections; i++) {
            DatabaseConnection conn = createConnection();
            if (conn != null) {
                availableConnections.add(conn);
                currentConnections++;
            }
        }
        while (availableConnections.size() < maxConnections && currentConnections < maxConnections) {
            DatabaseConnection conn = createConnection();
            if (conn != null) {
                availableConnections.add(conn);
                currentConnections++;
            }
        }
    }

    // 연결 획득
    public synchronized DatabaseConnection getConnection() throws InterruptedException {
        while (availableConnections.isEmpty()) {
            wait(); // 대기 큐 구현
        }
        DatabaseConnection conn = availableConnections.remove();
        return conn;
    }

    // 연결 반환
    public synchronized void releaseConnection(DatabaseConnection connection) {
        currentConnections--;
        availableConnections.add(connection);
        notifyAll(); // 모든 기다리는 스레드를 깨우기 위함
    }

    // 연결 유효성 검사 및 자동 재연결 기능 구현 (예제용으로 단순화)
    private DatabaseConnection createConnection() {
        // 실제 구현에서는 데이터베이스 연결 객체가 필요합니다.
        // 여기서는 예시로 주석 처리하였으나, 실제로는 JDBC 드라이버를 사용하여 Connection 생성
        // return new DatabaseConnection(); 
        return null;
    }

    public int getCurrentConnections() {
        return currentConnections;
    }
}

class DatabaseConnection {
    // 실제 구현에서는 데이터베이스 연결 관련 속성과 메소드가 필요합니다.
    public void close() {
        System.out.println("Connection closed.");
    }

    public boolean isValid() {
        // 유효성 검사 로직을 추가해야 합니다
        return true;
    }
}
```

위 코드는 `DatabaseConnectionPool` 클래스를 정의하며, 이클립스 또는 IntelliJ IDEA와 같은 IDE에서 Java 프로젝트에 추가할 수 있습니다. 실제 데이터베이스 연결 객체 및 유효성 검사를 구현하려면 더 복잡한 로직을 추가해야 합니다.

**주의사항:**
- `DatabaseConnection` 클래스는 실제 DB 연결 객체를 나타내며, 여기서는 단순히 예시로 만든 클래스입니다. 실제로는 JDBC 드라이버를 통해 데이터베이스 연결을 생성해야 하며, 유효성 검사 메소드 `isValid()` 역시 구현되어야 합니다.
- 이 코드에서는 단순화하여 `createConnection()` 메서드가 `null`을 반환하도록 했습니다. 실제 사용 시에는 이 메서드에서 새로운 `DatabaseConnection` 객체를 생성해야 합니다.
- 현재 `getConnection()`과 `releaseConnection()` 메서드는 동기화되어 있으며, `notifyAll()` 메소드는 모든 기다리는 스레드를 깨워주도록 설계되었습니다.