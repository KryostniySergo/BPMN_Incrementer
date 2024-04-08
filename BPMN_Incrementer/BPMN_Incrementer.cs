using System.Text.RegularExpressions;

public class BPMN_Incrimenter
{
    private string firstNumber;
    private string secondNumber;
    private string lastNumber;

    public BPMN_Incrimenter(Match userInput)
    {
        firstNumber = userInput.Groups[2].Value;
        secondNumber = userInput.Groups[3].Value;
        lastNumber = userInput.Groups[4].Value;
    }

    private string __choose_pattern()
    {
        if (!string.IsNullOrEmpty(lastNumber))
        {
            return $"name=\"(" + firstNumber + @"\." + secondNumber + @"\.?(\d{1,2})?)";
        }
        else if (!string.IsNullOrEmpty(secondNumber))
        {
            return $"name=\"(" + firstNumber + @"\.?(\d{1,2})?)";
        }
        else
        {
            return $"name=\"((" + firstNumber + @")\.)";
        }
    }

    private string __choose_replacment_str(Match match)
    {
        if (!string.IsNullOrEmpty(lastNumber))
        {
            return $"name=\"{firstNumber}.{secondNumber}.{int.Parse(match.Groups[2].Value) + 1}";
        }
        else if (!string.IsNullOrEmpty(secondNumber))
        {
            return $"name=\"{firstNumber}.{int.Parse(match.Groups[2].Value) + 1}";
        }
        else
        {
            return $"name=\"{int.Parse(match.Groups[2].Value) + 1}.";
        }
    }

    private bool __retry_or_continue(Match match)
    {
        if (!string.IsNullOrEmpty(lastNumber) && int.Parse(lastNumber) > int.Parse(match.Groups[2].Value))
        {
            return true;
        }
        else if (string.IsNullOrEmpty(lastNumber) && !string.IsNullOrEmpty(secondNumber) && int.Parse(secondNumber) > int.Parse(match.Groups[2].Value))
        {
            return true;
        }
        else if (string.IsNullOrEmpty(lastNumber) && string.IsNullOrEmpty(secondNumber) && int.Parse(firstNumber) < int.Parse(match.Groups[2].Value))
        {
            return true;
        }

        return false;
    }

    public void IncrimentStrings(string[] stringList)
    {
        string pattern = __choose_pattern();

        for (int i = 0; i < stringList.Length; i++)
        {
            Match match = Regex.Match(stringList[i], pattern);
            if (!match.Success)
            {
                continue;
            }
            if (__retry_or_continue(match))
            {
                continue;
            }

            string replacmentStr = __choose_replacment_str(match);

            stringList[i] = stringList[i].Replace(
                $"name=\"{match.Groups[1]}",
                replacmentStr
            );

        }
    }
}
