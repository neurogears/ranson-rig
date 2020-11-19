using Bonsai;
using System.ComponentModel;
using Bonsai.Osc;
using System.IO;
using Bonsai.IO;

[Combinator]
[Description("Writes OSC messages to a flat binary file.")]
[WorkflowElementCategory(ElementCategory.Sink)]
public class ArrayWriter : StreamSink<Message, BinaryWriter>
{
    protected override BinaryWriter CreateWriter(Stream stream)
    {
        return new BinaryWriter(stream);
    }

    protected override void Write(BinaryWriter writer, Message input)
    {
        var buffer = input.Buffer;
        writer.Write(buffer.Count);
        writer.Write(buffer.Array);
    }
}
