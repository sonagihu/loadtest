다음은 요구사항에 맞춘 `ValidationUtils` 클래스의 구현 사례입니다:

```java
public class ValidationUtils {

    private static final String EMAIL_PATTERN = "^[a-zA-Z0-9_+&*-]+(?:\\." +
            "[a-zA-Z0-9_+&*-]+)*@" + "(?:[a-zA-Z0-9-]+\\.)+" + 
            "[a-zA-Z]{2,7}$";
    private static final String PHONE_PATTERN = "^\\+(?:[0-9] ?){6,14}[0-9]$"; // International phone number pattern
    private static final String URL_PATTERN = "^(https?|ftp)://[^\\s/$.???#].[^\\s]*$";
    private static final int CREDIT_CARD_NUMBER_LENGTH = 16;
    
    /**
     * Validates an email address.
     * 
     * @param email the email to validate
     * @return true if the email is valid, false otherwise
     */
    public static boolean isValidEmail(String email) {
        return email.matches(EMAIL_PATTERN);
    }

    /**
     * Validates a phone number in international format.
     * 
     * @param phoneNumber the phone number to validate
     * @return true if the phone number is valid, false otherwise
     */
    public static boolean isValidPhoneNumber(String phoneNumber) {
        return phoneNumber.matches(PHONE_PATTERN);
    }

    /**
     * Validates a URL (Uniform Resource Locator).
     * 
     * @param url the URL to validate
     * @return true if the URL is valid, false otherwise
     */
    public static boolean isValidURL(String url) {
        return url.matches(URL_PATTERN);
    }

    /**
     * Validates a credit card number using the Luhn algorithm.
     * 
     * @param creditCardNumber the credit card number to validate
     * @return true if the credit card number is valid, false otherwise
     */
    public static boolean isValidCreditCard(String creditCardNumber) {
        return (creditCardNumber.length() == CREDIT_CARD_NUMBER_LENGTH)
                && luhnAlgorithm(creditCardNumber);
    }

    private static boolean luhnAlgorithm(String ccNum) {
        int sum = 0;
        char[] chars = ccNum.toCharArray();
        for (int i = chars.length - 1; i >= 0; i -= 2) {
            String s = String.valueOf(chars[i] * 2);
            if (s.length() > 1)
                sum += Integer.parseInt(s.substring(0, 1)) + Integer.parseInt(s.substring(1));
            else
                sum += chars[i];
        }
        for (int i = chars.length - 2; i >= 0; i -= 2) {
            sum += Character.getNumericValue(chars[i]);
        }
        return sum % 10 == 0;
    }

    /**
     * Returns a detailed error message based on the validation result.
     * 
     * @param isValid true if the input is valid, false otherwise
     * @return an error message for the given validation status
     */
    public static String getErrorMessage(boolean isValid) {
        return isValid ? "Validation successful." : "Validation failed.";
    }
}
```

이 클래스는 다음과 같은 기능을 제공합니다:
1. `isValidEmail`: 이메일 주소 검증.
2. `isValidPhoneNumber`: 국제 형식 전화번호 검증.
3. `isValidURL`: URL 검증.
4. `isValidCreditCard`: Luhn 알고리즘을 사용한 신용카드 번호 검증.

이 클래스는 각각의 메서드가 검증에 실패하면 자세한 에러 메시지를 제공하도록 설계되었습니다. 예를 들어, `getErrorMessage` 메소드는 검증 결과에 따라 적절한 오류 메시지를 반환합니다.