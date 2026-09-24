package kit.examples.idempotency;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.UUID;

/** Runs with only a JDK. Assertions throw explicitly; -ea is not required. */
public final class CommandFingerprintTest {
    private static final LocalDate DATE = LocalDate.of(2026, 9, 23);
    private static int passed;

    private CommandFingerprintTest() { }

    public static void main(String[] args) {
        test("independent-known-vector", () -> equal("bd2ea3b0e116bbd8d8e9bc338779825194f907d77d57cc2d8c1de8e298427242", hash("12.30", "Consulting")));
        test("repeat-stable", () -> equal(hash("12.30", "Consulting"), hash("12.30", "Consulting")));
        test("equivalent-numeric-scale", () -> equal(hash("12.3", "x"), hash("12.300", "x")));
        test("changed-amount", () -> different(hash("12.30", "x"), hash("12.31", "x")));
        test("changed-date", () -> different(hash("12.30", "x"),
                CommandFingerprint.of(new BigDecimal("12.30"), DATE.plusDays(1), "x")));
        test("exact-text", () -> different(hash("12.30", "x"), hash("12.30", " x")));
        test("unicode-round-trip", () -> equal(hash("12.30", "\u010d\uD83D\uDCB6"),
                hash("12.300", "\u010d\uD83D\uDCB6")));
        test("reject-zero", () -> rejects(IllegalArgumentException.class, () -> hash("0", "x")));
        test("reject-negative", () -> rejects(IllegalArgumentException.class, () -> hash("-1", "x")));
        test("reject-rounded-subcent", () -> rejects(IllegalArgumentException.class, () -> hash("1.001", "x")));
        test("reject-out-of-range", () -> {
            rejects(IllegalArgumentException.class, () -> hash("1000000000000", "x"));
            rejects(IllegalArgumentException.class, () -> hash("1E-100000", "x"));
            rejects(IllegalArgumentException.class, () -> hash("1E+100000", "x"));
        });
        test("maximum-exact-amount", () -> check(hash("999999999999.99", "x").matches("[0-9a-f]{64}")));
        test("null-inputs", () -> {
            rejects(NullPointerException.class, () -> CommandFingerprint.of(null, DATE, "x"));
            rejects(NullPointerException.class, () -> CommandFingerprint.of(BigDecimal.ONE, null, "x"));
            rejects(NullPointerException.class, () -> CommandFingerprint.of(BigDecimal.ONE, DATE, null));
        });
        test("description-bound", () -> {
            check(hash("1", "x".repeat(2048)).length() == 64);
            rejects(IllegalArgumentException.class, () -> hash("1", "x".repeat(2049)));
        });
        test("malformed-unicode", () -> {
            rejects(IllegalArgumentException.class, () -> hash("1", "\uD800"));
            rejects(IllegalArgumentException.class, () -> hash("1", "\uDC00"));
        });
        var a = UUID.fromString("00000000-0000-0000-0000-000000000001");
        var b = UUID.fromString("00000000-0000-0000-0000-000000000002");
        test("key-equality", () -> equal(new CommandFingerprint.RequestKey(a, "receipt:v1", "key-1"),
                new CommandFingerprint.RequestKey(a, "receipt:v1", "key-1")));
        test("key-owner-separation", () -> different(new CommandFingerprint.RequestKey(a, "receipt:v1", "key-1"),
                new CommandFingerprint.RequestKey(b, "receipt:v1", "key-1")));
        test("key-operation-separation", () -> different(new CommandFingerprint.RequestKey(a, "receipt:v1", "key-1"),
                new CommandFingerprint.RequestKey(a, "receipt:v2", "key-1")));
        test("key-validation", () -> {
            rejects(NullPointerException.class, () -> new CommandFingerprint.RequestKey(null, "op", "key"));
            rejects(IllegalArgumentException.class, () -> new CommandFingerprint.RequestKey(a, "op", ""));
            rejects(IllegalArgumentException.class, () -> new CommandFingerprint.RequestKey(a, "op", "x".repeat(129)));
            rejects(IllegalArgumentException.class, () -> new CommandFingerprint.RequestKey(a, "op", "x\n"));
        });
        test("key-operation-bound", () -> {
            new CommandFingerprint.RequestKey(a, "x".repeat(100), "x".repeat(128));
            rejects(IllegalArgumentException.class, () -> new CommandFingerprint.RequestKey(a, "x".repeat(101), "x"));
        });
        if (passed != 20) throw new AssertionError("Expected all 20 scenarios to execute");
        System.out.println("JAVA_HELPER_SCENARIOS_PASS=" + passed);
        System.out.println("SCOPE=fingerprint_and_key_value_only; DB_SPRING_SECURITY_NULLAWAY=NOT_RUN");
    }

    private static String hash(String amount, String description) {
        return CommandFingerprint.of(new BigDecimal(amount), DATE, description);
    }

    private static void test(String label, Runnable body) {
        try { body.run(); passed++; }
        catch (RuntimeException | AssertionError failure) { throw new AssertionError(label, failure); }
    }

    private static void check(boolean condition) {
        if (!condition) throw new AssertionError("Condition failed");
    }

    private static void equal(Object a, Object b) { check(a.equals(b)); }
    private static void different(Object a, Object b) { check(!a.equals(b)); }

    private static void rejects(Class<? extends Throwable> type, Runnable action) {
        try { action.run(); }
        catch (Throwable failure) {
            if (type.isInstance(failure)) return;
            throw new AssertionError("Wrong exception type", failure);
        }
        throw new AssertionError("Expected " + type.getSimpleName());
    }
}
