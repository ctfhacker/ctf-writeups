// Decompiled with JetBrains decompiler
// Type: Dialer
// Assembly: dial, Version=0.0.0.0, Culture=neutral, PublicKeyToken=null
// MVID: 6BF6FF42-F044-4743-B8CC-E6ED08CCD84D
// Assembly location: Z:\vmshare\ctf\houseccon\dial.exe

using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;

namespace Dialer{
class Dialer
{
  private static string msg = "EAAAADbcv071xsm2a1TSsH272dzbziJOuOiSmqK0Qkr89PYeZ5H8m7pOhQtnzgtFoVGnKQ==";

  private static string[] Answers = new string[25]
  {
    "Hello? Hello? Is anybody there?",
    "Hello?",
    "Hello?",
    "Hello?",
    "Hello?",
    "Hello?",
    "Hello?",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "Hello, who is this?",
    "Hello, who's calling?",
    "Hotel Operator, how may I connect you?",
    "Maple Tree Inn, how may I direct your call?",
    "Hello, Vagabond in, how may I direct your call?",
    "Saul's fish market?",
    "Tucker, Beevan and Lawson law firm, how can I",
    "Hello, this is mister Liam?",
    "Protovision inc, may I help you?",
    "Crystal Palace, may I take your order?",
    "Mckittrick speaking"
  };

  public static void Main()
  {
	long i;
    string words;
    while (true)
    {
		for(i = LOWVALUE; i < HIGHVALUE; i++){
			//Console.WriteLine(i);
			//Console.WriteLine("Dialing {0}...", (object) matchCollection[0].Groups[1].Value);
			//Thread.Sleep(2000);
			///Console.WriteLine("bbb");
			words = Dialer.Dial(i);
			if (string.IsNullOrEmpty(words))
			{
			  //int index = random.Next(0, Dialer.Answers.Length);
			  if (Dialer.Answers[2] == "")
			  {
				Thread.Sleep(1);
			  }
			  else
			  {
				//Console.WriteLine("Connect");
				Thread.Sleep(1);
				//spVoice.Speak(Dialer.Answers[index], SpeechVoiceSpeakFlags.SVSFDefault);
			  }
			  //Console.WriteLine("No carrier");
			  ///Console.WriteLine("ddd");
			}
			else{
				string path = @"outputLOWVALUE.txt";
				// This text is added only once to the file. 
				// Create a file to write to. 
				using (StreamWriter sw = File.AppendText(path)) 
				{
					sw.WriteLine(i);
					sw.WriteLine(words);
					//sw.WriteLine("Welcome");
				}	
			
				Console.WriteLine("AAAAAAAA");
				Console.WriteLine(i);
				Console.WriteLine(words);
			}
		}
		//Console.WriteLine("ccc");
    }
  }


  public static string Dial(long dialnum)
  {
    string str = "";
    byte[] bytes = (byte[]) null;
    try
    {
      bytes = Dialer.DecodeB64AesString(Dialer.msg, dialnum.ToString());
    }
    catch (Exception ex)
    {
    }
    if (bytes != null)
      str = Encoding.UTF8.GetString(bytes);
    return str;
  }

  private static void ResetConsole()
  {
    Console.BackgroundColor = ConsoleColor.Black;
    Console.ForegroundColor = ConsoleColor.Gray;
    Console.CursorSize = 10;
  }

  private static void CloseTerminal()
  {
    Console.WriteLine("\n+++ATH0");
    Thread.Sleep(2000);
    Dialer.ResetConsole();
  }

  private static void ctrlc(object sender, ConsoleCancelEventArgs args)
  {
    Dialer.CloseTerminal();
  }

  public static byte[] DecodeB64AesString(string b64cipherText, string sharedSecret)
  {
    byte[] bytes = Encoding.ASCII.GetBytes("j7Hxz;P,3*hzz0");
    if (string.IsNullOrEmpty(b64cipherText))
      throw new ArgumentNullException("b64cipherText");
    if (string.IsNullOrEmpty(sharedSecret))
      throw new ArgumentNullException("sharedSecret");
    RijndaelManaged rijndaelManaged = (RijndaelManaged) null;
    byte[] numArray = (byte[]) null;
    try
    {
      Rfc2898DeriveBytes rfc2898DeriveBytes = new Rfc2898DeriveBytes(sharedSecret, bytes);
      using (MemoryStream memoryStream = new MemoryStream(Convert.FromBase64String(b64cipherText)))
      {
        rijndaelManaged = new RijndaelManaged();
        rijndaelManaged.Key = rfc2898DeriveBytes.GetBytes(rijndaelManaged.KeySize / 8);
        rijndaelManaged.IV = Dialer.ReadByteArray((Stream) memoryStream);
        ICryptoTransform decryptor = rijndaelManaged.CreateDecryptor(rijndaelManaged.Key, rijndaelManaged.IV);
        using (CryptoStream cryptoStream = new CryptoStream((Stream) memoryStream, decryptor, CryptoStreamMode.Read))
        {
          byte[] buffer = new byte[b64cipherText.Length];
          int length = cryptoStream.Read(buffer, 0, buffer.Length);
          numArray = new byte[length];
          Array.Copy((Array) buffer, 0, (Array) numArray, 0, length);
        }
      }
    }
    finally
    {
      if (rijndaelManaged != null)
        rijndaelManaged.Clear();
    }
    return numArray;
  }

  private static byte[] ReadByteArray(Stream s)
  {
    byte[] buffer1 = new byte[4];
    if (s.Read(buffer1, 0, buffer1.Length) != buffer1.Length)
      throw new SystemException("Stream did not contain properly formatted byte array");
    byte[] buffer2 = new byte[BitConverter.ToInt32(buffer1, 0)];
    if (s.Read(buffer2, 0, buffer2.Length) != buffer2.Length)
      throw new SystemException("Did not read byte array properly");
    return buffer2;
  }
}
}
