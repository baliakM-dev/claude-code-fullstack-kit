package kit.examples.idempotency;

import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.time.LocalDate;
import java.util.HexFormat;
import java.util.Objects;
import java.util.UUID;

/**
 * Newly authored illustrative helper, not a persistence or security implementation.
 * Example contract: positive EUR value, up to 12 integral digits and exact cents (precision and absolute scale each at most 64);
 * ISO LocalDate; exact description text up to 2048 UTF-16 code units, valid Unicode.
 * Not a tax-rounding policy. SQL claim/replay, authentication and CSRF are external.
 */
public final class CommandFingerprint {
    private static final String CONTRACT = "receipt:v1";

    private CommandFingerprint() { }

    /** Owner comes from trusted server identity mapping, never a client owner field. */
    public record RequestKey(UUID ownerId, String operation, String clientKey) {
        public RequestKey {
            Objects.requireNonNull(ownerId, "ownerId");
            requireIdentifier(operation, 100, "operation");
            requireIdentifier(clientKey, 128, "clientKey");
        }
    }

    public static String of(BigDecimal amount, LocalDate businessDate, String description) {
        Objects.requireNonNull(amount, "amount");
        Objects.requireNonNull(businessDate, "businessDate");
        Objects.requireNonNull(description, "description");
        if (amount.signum() <= 0 || amount.precision() > 64 || Math.abs((long) amount.scale()) > 64
                || (long) amount.precision() - amount.scale() > 12) {
            throw new IllegalArgumentException("amount must be positive and within the example bound");
        }
        final BigDecimal exactCents;
        try {
            exactCents = amount.setScale(2, RoundingMode.UNNECESSARY);
        } catch (ArithmeticException invalidScale) {
            throw new IllegalArgumentException("amount cannot require rounding", invalidScale);
        }
        if (description.length() > 2048) {
            throw new IllegalArgumentException("description exceeds the example bound");
        }
        requireValidUnicode(description);
        try {
            var buffer = new ByteArrayOutputStream();
            try (var out = new DataOutputStream(buffer)) {
                // Length-prefix UTF-8 fields: no delimiter ambiguity and no raw JSON dependence.
                writeField(out, CONTRACT);
                writeField(out, "EUR");
                writeField(out, exactCents.toPlainString());
                writeField(out, businessDate.toString());
                writeField(out, description);
            }
            return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256")
                    .digest(buffer.toByteArray()));
        } catch (IOException | NoSuchAlgorithmException impossibleInStandardRuntime) {
            throw new IllegalStateException("Unable to construct fingerprint", impossibleInStandardRuntime);
        }
    }

    private static void writeField(DataOutputStream out, String value) throws IOException {
        byte[] bytes = value.getBytes(StandardCharsets.UTF_8);
        out.writeInt(bytes.length);
        out.write(bytes);
    }

    private static void requireIdentifier(String value, int maxLength, String field) {
        Objects.requireNonNull(value, field);
        if (value.isEmpty() || value.length() > maxLength || !value.matches("[A-Za-z0-9._:-]+")) {
            throw new IllegalArgumentException(field + " is outside the example identifier contract");
        }
    }

    private static void requireValidUnicode(String value) {
        for (int i = 0; i < value.length(); i++) {
            char c = value.charAt(i);
            if (Character.isHighSurrogate(c)) {
                if (i + 1 >= value.length() || !Character.isLowSurrogate(value.charAt(i + 1))) {
                    throw new IllegalArgumentException("description has an unpaired surrogate");
                }
                i++;
            } else if (Character.isLowSurrogate(c)) {
                throw new IllegalArgumentException("description has an unpaired surrogate");
            }
        }
    }
}
