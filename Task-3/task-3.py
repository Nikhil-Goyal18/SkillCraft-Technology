import re
import string

class PasswordStrengthChecker:
    def __init__(self, min_length=8):
        self.min_length = min_length
        self.special_chars = string.punctuation

    def has_lowercase(self, pwd):
        return bool(re.search(r"[a-z]", pwd))

    def has_uppercase(self, pwd):
        return bool(re.search(r"[A-Z]", pwd))

    def has_digit(self, pwd):
        return bool(re.search(r"\d", pwd))

    def has_special_char(self, pwd):
        return bool(re.search(rf"[{re.escape(self.special_chars)}]", pwd))

    def has_no_repeated_chars(self, pwd, repeat_limit=3):
        pattern = r"(.)\1{" + str(repeat_limit) + ",}"
        return re.search(pattern, pwd) is None

    def has_no_sequences(self, pwd, seq_length=3):
        if len(pwd) < seq_length:
            return True

        sequences = []
        alphabet = string.ascii_lowercase
        digits = string.digits

        for i in range(len(alphabet) - seq_length + 1):
            sequences.append(alphabet[i:i+seq_length])
            sequences.append(alphabet[i:i+seq_length][::-1])

        for i in range(len(digits) - seq_length + 1):
            sequences.append(digits[i:i+seq_length])
            sequences.append(digits[i:i+seq_length][::-1])

        pwd_lower = pwd.lower()
        for i in range(len(pwd_lower) - seq_length + 1):
            segment = pwd_lower[i:i+seq_length]
            if segment in sequences:
                return False
        return True

    def assess_strength(self, password):
        issues = {}

        issues['Too Short (< {} chars)'.format(self.min_length)] = len(password) < self.min_length
        issues['Missing Lowercase'] = not self.has_lowercase(password)
        issues['Missing Uppercase'] = not self.has_uppercase(password)
        issues['Missing Digit'] = not self.has_digit(password)
        issues['Missing Special Character'] = not self.has_special_char(password)
        issues['Repeated Characters (>3 times consecutively)'] = not self.has_no_repeated_chars(password)
        issues['Sequential Characters (3 or more)'] = not self.has_no_sequences(password)

        score = 10

        deductions = {
            'Too Short (< {} chars)'.format(self.min_length): 4,
            'Missing Lowercase': 1,
            'Missing Uppercase': 1,
            'Missing Digit': 2,
            'Missing Special Character': 2,
            'Repeated Characters (>3 times consecutively)': 2,
            'Sequential Characters (3 or more)': 2,
        }

        for issue, present in issues.items():
            if present:
                score -= deductions.get(issue, 0)

        score = max(0, min(score, 10))

        if score >= 9:
            strength = "Very Strong"
        elif score >= 7:
            strength = "Strong"
        elif score >= 5:
            strength = "Moderate"
        elif score >= 3:
            strength = "Weak"
        else:
            strength = "Very Weak"

        return {
            "Password": password,
            "Score": score,
            "Strength": strength,
            "Issues": issues
        }

def main():
    print("Advanced Password Strength Checker\n")
    checker = PasswordStrengthChecker(min_length=8)

    while True:
        pwd = input("Enter a password to assess (or 'exit' to quit): ")
        if pwd.lower() == 'exit':
            print("Exiting...")
            break

        result = checker.assess_strength(pwd)

        print("\nPassword Strength Report:")
        print(f"Password: {result['Password']}")
        print(f"Score: {result['Score']}/10")
        print(f"Strength Level: {result['Strength']}")
        print("Issues Found:")
        for issue, present in result['Issues'].items():
            print(f" - {issue}: {'Yes' if present else 'No'}")

        print("\n" + "-"*40 + "\n")

if __name__ == "__main__":
    main()
