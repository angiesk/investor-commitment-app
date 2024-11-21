export const roundAmount = (amount: number): string => {
  if (amount >= 1_000_000_000) {
    return (amount / 1_000_000_000).toFixed(1) + "B"; // Billion
  } else if (amount >= 1_000_000) {
    return (amount / 1_000_000).toFixed(1) + "M"; // Million
  } else {
    return amount.toFixed(0); // Keep the exact value if less than a million
  }
};

export const calculateTotalCommitments = (
  commitments: { amount: number; currency: string }[],
  targetCurrency: string = "GBP"
): number => {
  return commitments
    .filter((commitment) => commitment.currency === targetCurrency)
    .reduce((sum, commitment) => sum + commitment.amount, 0);
};
