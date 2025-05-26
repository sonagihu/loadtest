아래는 위 요구사항들을 모두 충족하는 `CacheManager` 클래스의 구현 예입니다.

```java
import java.util.LinkedHashMap;
import java.util.Map;

public class CacheManager {

    private final Map<Integer, Integer> cache;
    private int maxSize;

    public CacheManager(int maxSize) {
        this.maxSize = maxSize;
        // LinkedHashMap 에서는 accessOrder 옵션을 true 로 설정하여 LRU 동작을 구현합니다.
        this.cache = new LinkedHashMap<>(maxSize, 0.75f, true) {
            @Override
            protected boolean removeEldestEntry(Map.Entry<Integer, Integer> eldest) {
                return size() > maxSize;
            }
        };
    }

    // 캐시 항목 추가 (put)
    public synchronized void put(Integer key, Integer value) {
        cache.put(key, value);
    }

    // 캐시 항목 조회 (get)
    public synchronized Integer get(Integer key) {
        return cache.get(key);
    }

    // 캐시 항목 제거 (remove)
    public synchronized void remove(Integer key) {
        cache.remove(key);
    }

    // 캐시 크기 조회 (size)
    public synchronized int size() {
        return cache.size();
    }
}
```

### 설명:
1. **클래스 정의**: `CacheManager` 클래스는 주어진 최대 크기를 가지는 LRU 캐시를 구현합니다.
2. **인스턴스 변수**:
   - `cache`: `LinkedHashMap`을 사용하여 항목들을 저장하고, `accessOrder` 옵션을 `true`로 설정하여 LRU 동작을 구현합니다.
   - `maxSize`: 캐시의 최대 크기를 저장하는 변수입니다.
3. **생성자**:
   - 생성자는 `LinkedHashMap` 인스턴스를 초기화하고, `removeEldestEntry` 메서드를 오버라이드하여 최대 크기를 초과하면 가장 오래된 항목을 자동으로 제거하도록 합니다.
4. **메서드 구현**:
   - `put`: 캐시에 항목을 추가합니다.
   - `get`: 캐시에서 항목을 조회하고, 조회할 때마다 해당 항목이 가장 최근에 사용되었다고 간주하여 위치가 앞으로 당겨집니다.
   - `remove`: 캐시에서 항목을 제거합니다.
   - `size`: 현재 캐시 크기를 반환합니다.

### 스레드 안전성:
- `put`, `get`, `remove`, `size` 메서드 모두 `synchronized` 키워드로 작성되어 스레드 간의 충돌을 방지하고, 여러 스레드가 동시에 캐시에 접근할 때 데이터 일관성을 보장합니다.