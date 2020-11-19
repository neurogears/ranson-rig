using Bonsai;
using System;
using System.ComponentModel;
using System.Collections.Generic;
using System.Reactive.Linq;
using Bonsai.Osc;
using System.IO;

[Combinator]
[Description("Reads OSC messages from a flat binary file.")]
[WorkflowElementCategory(ElementCategory.Source)]
public class ArrayReader
{
    [Editor("Bonsai.Design.OpenFileNameEditor, Bonsai.Design", DesignTypes.UITypeEditor)]
    public string FileName { get; set; }

    IEnumerable<Message> ReadAllMessages(string path)
    {
        using (var stream = File.OpenRead(path))
        using (var reader = new BinaryReader(stream))
        {
            while (true)
            {
                int count;
                try { count = reader.ReadInt32(); }
                catch (EndOfStreamException) { break; }
                
                var buffer = new byte[count];
                reader.Read(buffer, 0, count);
                yield return new Message(buffer);
            }
        }
    }

    public IObservable<Message> Process()
    {
        return ReadAllMessages(FileName).ToObservable();
    }
}
