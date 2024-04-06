using System;
using System.IO;
using System.Text.RegularExpressions;

namespace BPMN_Incrementer
{
    internal class Utils
    {
        public string CreateNewBpmn(string bpmnPath)
        {
            string folderPath = Path.GetDirectoryName(bpmnPath);
            string filePath = Path.Combine(folderPath, "new.bpmn");
            return filePath;
        }

        public string[] GetStringFromBpmn(string bpmnPath)
        {
            return File.ReadAllLines(bpmnPath);
        }

        public void Rewrite_new_bpmn(string new_bpmn_path, string[] raw_string)
        {
            File.WriteAllLines(new_bpmn_path, raw_string);
        }

        public Match ValidateInput(string inputStr)
        {
            string pattern = @"((\d{1,2})\.(\d{1,2})?\.?(\d{1,2})?)";
            Match match = Regex.Match(inputStr, pattern);

            if (!match.Success)
            {
                throw new Exception(
                    "Ваше значение не подходит шаблону!\nВведите корректные даные. Например 5. или 5.1 или 4.2.5 "
                );
            }

            return match;
        }
    }
}
