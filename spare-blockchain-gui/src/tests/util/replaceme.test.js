const replaceme = require('../../util/replaceme');

describe('replaceme', () => {
  it('converts number mojo to replaceme', () => {
    const result = replaceme.mojo_to_replaceme(1000000);

    expect(result).toBe(0.000001);
  });
  it('converts string mojo to replaceme', () => {
    const result = replaceme.mojo_to_replaceme('1000000');

    expect(result).toBe(0.000001);
  });
  it('converts number mojo to replaceme string', () => {
    const result = replaceme.mojo_to_replaceme_string(1000000);

    expect(result).toBe('0.000001');
  });
  it('converts string mojo to replaceme string', () => {
    const result = replaceme.mojo_to_replaceme_string('1000000');

    expect(result).toBe('0.000001');
  });
  it('converts number replaceme to mojo', () => {
    const result = replaceme.replaceme_to_mojo(0.000001);

    expect(result).toBe(1000000);
  });
  it('converts string replaceme to mojo', () => {
    const result = replaceme.replaceme_to_mojo('0.000001');

    expect(result).toBe(1000000);
  });
  it('converts number mojo to colouredcoin', () => {
    const result = replaceme.mojo_to_colouredcoin(1000000);

    expect(result).toBe(1000);
  });
  it('converts string mojo to colouredcoin', () => {
    const result = replaceme.mojo_to_colouredcoin('1000000');

    expect(result).toBe(1000);
  });
  it('converts number mojo to colouredcoin string', () => {
    const result = replaceme.mojo_to_colouredcoin_string(1000000);

    expect(result).toBe('1,000');
  });
  it('converts string mojo to colouredcoin string', () => {
    const result = replaceme.mojo_to_colouredcoin_string('1000000');

    expect(result).toBe('1,000');
  });
  it('converts number colouredcoin to mojo', () => {
    const result = replaceme.colouredcoin_to_mojo(1000);

    expect(result).toBe(1000000);
  });
  it('converts string colouredcoin to mojo', () => {
    const result = replaceme.colouredcoin_to_mojo('1000');

    expect(result).toBe(1000000);
  });
});
