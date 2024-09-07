from scipy.stats import binom

SYMBOL = 8
CODEWORD = 255 * SYMBOL
MESSAGE = 239 * SYMBOL
CAPABILITY = (CODEWORD - MESSAGE) // SYMBOL // 2

ERROR_RATE = 0.001
print(f"Prev FEC bits error rate:\t{ERROR_RATE :.16f}")

symbol_error_indices = SYMBOL + 1
symbol_error_rate = [0] * symbol_error_indices
for i in range(symbol_error_indices):
    symbol_error_rate[i] = binom.pmf(i, SYMBOL, ERROR_RATE)
    # print(f"{i}-errors-symbol rate:\t\t{symbol_error_rate[i] :.16f}")
prev_fec_symbols_error_rate = 1 - symbol_error_rate[0]
print(f"Prev FEC symbols error rate:\t{prev_fec_symbols_error_rate :.16f}")

message_error_indices = int(MESSAGE / SYMBOL) + 1
message_error_rate = [0] * message_error_indices
for i in range(message_error_indices):
    message_error_rate[i] = binom.pmf(i, MESSAGE / SYMBOL, prev_fec_symbols_error_rate)
    # print(f"{i :03d}-errors-message rate:\t{message_error_rate[i] :.16f}")
prev_fec_message_error_rate = 1 - message_error_rate[0]
print(f"Prev FEC message error rate:\t{prev_fec_message_error_rate :.16f}")

post_fec_message_error_rate = sum(message_error_rate[i] if i > CAPABILITY else 0 for i in range(message_error_indices))
print(f"Post FEC message error rate:\t{post_fec_message_error_rate :.16f}")

post_fec_symbols_error_rate = sum((i if i > CAPABILITY else 0) * message_error_rate[i] for i in range(message_error_indices)) / (MESSAGE // SYMBOL)
print(f"Post FEC symbols error rate:\t{post_fec_symbols_error_rate :.16f}")

post_fec_bits_error_rate = post_fec_symbols_error_rate * sum(i * symbol_error_rate[i] / prev_fec_symbols_error_rate for i in range(symbol_error_indices)) / SYMBOL
print(f"Post FEC bits error rate:\t{post_fec_bits_error_rate :.16f}")


