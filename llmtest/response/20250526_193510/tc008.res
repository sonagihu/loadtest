다음은 `RateLimiter` 클래스를 작성한 예제입니다. 이 클래스는 토큰 버킷 알고리즘을 사용하여 API 요청 제한을 구현하고, 다양한 시간 단위로 제한을 설정할 수 있도록 하였습니다.

```java
import java.time.Duration;
import java.util.concurrent.TimeUnit;

public class RateLimiter {

    private final String clientId;
    private double tokens;
    private double capacity;
    private double refillRatePerSecond; // 토큰 재충전 속도 (초당)
    private Duration cooldownPeriod;   // 재시작 기간
    private long lastRefillTime;

    public RateLimiter(String clientId, double initialCapacity, double refillRate, TimeUnit unit) {
        this.clientId = clientId;
        capacity = initialCapacity;
        refillRatePerSecond = unit.toSeconds(refillRate);
        tokens = initialCapacity; // 초기 토큰 수와 재충전 속도를 설정합니다.
        lastRefillTime = System.currentTimeMillis();
    }

    public boolean allowRequest() {
        if (tokens < 1) {
            return false;
        }
        refillTokens();
        tokens--;
        return true;
    }

    private void refillTokens() {
        long currentTimeMillis = System.currentTimeMillis();

        // 시간이 지난 만큼 토큰을 재충전합니다.
        long timeElapsed = (currentTimeMillis - lastRefillTime) / 1000; // seconds
        tokens += timeElapsed * refillRatePerSecond;
        if (tokens > capacity) {
            tokens = capacity;
        }
        
        lastRefillTime = currentTimeMillis;
    }

    public void setCooldownPeriod(Duration period) {
        this.cooldownPeriod = period;
    }

    public Duration getCooldownPeriod() {
        return cooldownPeriod != null ? cooldownPeriod : Duration.ofSeconds((long)(1 / refillRatePerSecond));
    }
    
    // 다른 설정 메서드도 추가할 수 있습니다.
}

```

이 클래스는 다음과 같은 기능을 구현하고 있습니다:

- `RateLimiter` 생성자: 클라이언트 식별자를 통해 각 클라이언트를 구분하고, 초기 토큰 수와 재충전 속도를 설정합니다. 
- `allowRequest`: 요청이 허용되는지 판단하며, 토큰이 부족하면 거부합니다.
- `refillTokens`: 시간 경과에 따라 토큰을 자동으로 재충전하는 로직입니다.
- `setCooldownPeriod`와 `getCooldownPeriod`: 재시작 기간 설정 및 가져오기 메서드. 이 기능은 클라이언트가 요청을 다시 시도하기 전에 필요한 대기 시간을 나타낼 수 있습니다.

이 클래스는 다양한 시간 단위(초/분/시간)로 제한을 설정할 수 있도록 `TimeUnit` 인수를 사용하고 있으며, 각 클라이언트의 토큰 버킷을 독립적으로 관리하여 여러 클라이언트의 요청을 구분할 수 있습니다.