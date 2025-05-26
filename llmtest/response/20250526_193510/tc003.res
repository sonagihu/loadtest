아래는 `ThreadPoolManager` 클래스를 작성한 예제입니다. 이 클래스는 Java의 `ExecutorService`와 관련된 인터페이스 및 구현체를 사용하여 스레드 풀을 생성, 관리하고 작업을 제출하며 취소할 수 있습니다.

```java
import java.util.concurrent.*;

public class ThreadPoolManager {
    private final ExecutorService executorService;

    public ThreadPoolManager(int corePoolSize) {
        this.executorService = new ThreadPoolExecutor(
                corePoolSize, corePoolSize,
                0L, TimeUnit.MILLISECONDS,
                new LinkedBlockingQueue<Runnable>());
    }

    public ThreadPoolManager(int corePoolSize, int maximumPoolSize) {
        this.executorService = new ThreadPoolExecutor(
                corePoolSize, maximumPoolSize,
                60L, TimeUnit.SECONDS,
                new LinkedBlockingQueue<>(1024),
                new NamedThreadFactory("ThreadPoolManager-"));
    }

    public void submit(Runnable task) {
        executorService.submit(task);
    }

    public boolean cancel(Runnable task) {
        return executorService.shutdownNow().contains(task);
    }

    public void shutdown() {
        executorService.shutdown();
    }

    public static class NamedThreadFactory implements ThreadFactory {
        private final String prefix;
        private int threadId = 0;

        public NamedThreadFactory(String prefix) {
            this.prefix = prefix;
        }

        @Override
        public Thread newThread(Runnable r) {
            return new Thread(r, prefix + "-" + threadId++);
        }
    }

    public void setCorePoolSize(int corePoolSize) {
        if (!executorService.isShutdown()) {
            ((ThreadPoolExecutor) executorService).setCorePoolSize(corePoolSize);
        }
    }

    public void setMaximumPoolSize(int maximumPoolSize) {
        if (!executorService.isShutdown()) {
            ((ThreadPoolExecutor) executorService).setMaximumPoolSize(maximumPoolSize);
        }
    }

    // 작업 상태 모니터링 기능
    public int getActiveCount() {
        return ((ThreadPoolExecutor) executorService).getActiveCount();
    }

    public int getLargestPoolSize() {
        return ((ThreadPoolExecutor) executorService).getLargestPoolSize();
    }

    public long getCompletedTaskCount() {
        return ((ThreadPoolExecutor) executorService).getCompletedTaskCount();
    }
}
```

### 설명
1. **스레드 풀 생성**: `ThreadPoolManager`는 두 가지 생성자로 제공되며, 각각 다르게 설정된 코어 스레드 수와 최대 스레드 수를 받아들입니다.
2. **작업 제출 (submit)**: `submit(Runnable task)` 메서드를 통해 작업을 스레드 풀에 제출할 수 있습니다.
3. **작업 취소 (cancel)**: `cancel(Runnable task)` 메서드는 주어진 작업을 취소하려고 시도합니다.
4. **스레드 풀 종료 (shutdown)**: `shutdown()` 메서드를 통해 스레드 풀의 실행을 종료할 수 있습니다.
5. **동적 설정 변경**: `setCorePoolSize`와 `setMaximumPoolSize` 메서드로 스레드 풀의 설정을 동적으로 변경할 수 있습니다.
6. **작업 상태 모니터링**: `getActiveCount()`, `getLargestPoolSize()`, `getCompletedTaskCount()` 메서드를 통해 현재 활성화된 스레드 수, 최대 총 스레드 수, 완료된 작업 수 등을 얻을 수 있습니다.

이 클래스는 Java 8 이상에서 동작하며, 필요한 모든 기능을 제공합니다.