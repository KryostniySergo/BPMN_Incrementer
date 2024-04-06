using System;
using System.Text.RegularExpressions;

namespace BPMN_Incrementer
{
    internal class Program
    {
        static void Main(string[] args)
        {
            var utils = new Utils();

            Console.Write("Введите путь до файла bpmn:\n");
            string bpmnPath = Console.ReadLine();

            string[] stringList = utils.GetStringFromBpmn(bpmnPath);

            Console.Write("С какого пункта начать? Например 5. или 5.1 или 4.2.5\n");
            string userInput = Console.ReadLine();

            Match match = utils.ValidateInput(userInput);
            BPMN_Incrimenter incrimenter = new BPMN_Incrimenter(match);
            incrimenter.IncrimentStrings(stringList);

            string newFilePath = utils.CreateNewBpmn(bpmnPath);
            utils.Rewrite_new_bpmn(newFilePath, stringList);
        }
    }
}
