다음은 `EncryptionUtils` 클래스를 작성한 예제입니다:

```java
import javax.crypto.Cipher;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.SecretKeySpec;
import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.util.Base64;
import org.apache.commons.codec.digest.DigestUtils;

public class EncryptionUtils {

    private static final String ALGORITHM_AES = "AES";
    private static final String ALGORITHM_RSA = "RSA";
    private static final String TRANSFORMATION_RSA = "RSA/NONE/PKCS1Padding";
    private static final String TRANSFORMATION_AES = "AES/ECB/PKCS5Padding";
    private static final int PBKDF2_ITERATIONS = 65536;
    private static final int AES_KEY_SIZE = 256;

    public static String aesEncrypt(String data, String key) throws Exception {
        byte[] encryptedBytes = encrypt(data.getBytes(), key);
        return Base64.getEncoder().encodeToString(encryptedBytes);
    }

    public static String aesDecrypt(String encryptedData, String key) throws Exception {
        byte[] decryptedBytes = decrypt(Base64.getDecoder().decode(encryptedData), key);
        return new String(decryptedBytes);
    }

    private static byte[] encrypt(byte[] data, String key) throws Exception {
        Cipher cipher = Cipher.getInstance(TRANSFORMATION_AES);
        SecretKeySpec keySpec = new SecretKeySpec(key.getBytes(), ALGORITHM_AES);
        cipher.init(Cipher.ENCRYPT_MODE, keySpec);
        return cipher.doFinal(data);
    }

    private static byte[] decrypt(byte[] encryptedData, String key) throws Exception {
        Cipher cipher = Cipher.getInstance(TRANSFORMATION_AES);
        SecretKeySpec keySpec = new SecretKeySpec(key.getBytes(), ALGORITHM_AES);
        cipher.init(Cipher.DECRYPT_MODE, keySpec);
        return cipher.doFinal(encryptedData);
    }

    public static String rsaEncrypt(String data, KeyPair publicKey) throws Exception {
        byte[] encryptedBytes = encrypt(data.getBytes(), publicKey);
        return Base64.getEncoder().encodeToString(encryptedBytes);
    }

    public static String rsaDecrypt(String encryptedData, PrivateKey privateKey) throws Exception {
        byte[] decryptedBytes = decrypt(Base64.getDecoder().decode(encryptedData), privateKey);
        return new String(decryptedBytes);
    }

    private static byte[] encrypt(byte[] data, KeyPair keyPair) throws Exception {
        Cipher cipher = Cipher.getInstance(TRANSFORMATION_RSA);
        cipher.init(Cipher.ENCRYPT_MODE, keyPair.getPublic());
        return cipher.doFinal(data);
    }

    private static byte[] decrypt(byte[] encryptedData, PrivateKey privateKey) throws Exception {
        Cipher cipher = Cipher.getInstance(TRANSFORMATION_RSA);
        cipher.init(Cipher.DECRYPT_MODE, privateKey);
        return cipher.doFinal(encryptedData);
    }

    public static String hashSHA256(String data) {
        return DigestUtils.sha256Hex(data);
    }

    public static String hashSHA512(String data) {
        return DigestUtils.sha512Hex(data);
    }

    public static String pbkdf2Hash(String password, byte[] salt) throws Exception {
        PBEKeySpec spec = new PBEKeySpec(password.toCharArray(), salt, PBKDF2_ITERATIONS, AES_KEY_SIZE);
        SecretKeyFactory skf = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA1");
        byte[] hash = skf.generateSecret(spec).getEncoded();
        return Base64.getEncoder().encodeToString(hash);
    }

    public static void main(String[] args) throws Exception {
        // 테스트 코드
        String key = "mySecretKey";
        KeyPairGenerator kpg = KeyPairGenerator.getInstance("RSA");
        kpg.initialize(2048, new SecureRandom());
        KeyPair keyPair = kpg.generateKeyPair();

        System.out.println("AES 암호화: " + aesEncrypt("hello", key));
        System.out.println("AES 복호화: " + aesDecrypt(aesEncrypt("hello", key), key));

        System.out.println("RSA 암호화: " + rsaEncrypt("world", keyPair.getPublic()));
        System.out.println("RSA 복호화: " + rsaDecrypt(rsaEncrypt("world", keyPair.getPublic()), keyPair.getPrivate()));

        System.out.println("SHA-256 해시: " + hashSHA256("test"));
        System.out.println("SHA-512 해시: " + hashSHA512("test"));

        byte[] salt = new byte[32];
        new SecureRandom().nextBytes(salt);
        System.out.println("PBKDF2 해싱: " + pbkdf2Hash("password", salt));
    }
}
```

이 클래스는 주어진 요구사항을 충족하는 `EncryptionUtils` 클래스입니다. 주요 기능은 다음과 같습니다:

1. AES 암호화/복호화
2. RSA 암호화/복호화 (공개키와 개인키를 사용)
3. SHA-256과 SHA-512 해시 함수 구현
4. PBKDF2 비밀번호 해싱
5. Base64 인코딩/디코딩

주의: RSA 암호화는 복잡한 키 관리 요구사항을 가집니다 (예: 공개키와 개인키 생성 및 관리). 이 예제에서는 간단하게 KeyPairGenerator를 사용하여 키 쌍을 생성하고 있습니다. 실제 적용시에는 보다 세밀한 키 관리를 위한 방법이 필요할 수 있습니다.

또한, AES 암호화는 ECB 모드로 간단히 처리하였지만, 실제 사용 시 ECB 대신 CBC 또는 GCM 등 더 안전한 모드를 권장합니다.