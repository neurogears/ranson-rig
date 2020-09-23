using Bonsai;
using System.ComponentModel;
using System.Collections.Generic;
using System.Linq;
using Bonsai.Resources;
using System.IO;
using Bonsai.Shaders.Configuration;

[Combinator]
[Description("Creates a collection of image sequences from the specified image folder.")]
[WorkflowElementCategory(ElementCategory.Combinator)]
public class VideoFolder : ResourceLoader
{
    [Description("The path to search.")]
    [Editor("Bonsai.Design.FolderNameEditor, Bonsai.Design", DesignTypes.UITypeEditor)]
    public string Path { get; set; }

    protected override IEnumerable<IResourceConfiguration> GetResources()
    {
        foreach (var entry in Directory.EnumerateDirectories(Path))
        {
            var frame = Directory.EnumerateFiles(entry).FirstOrDefault();
            if (frame != null)
            {
                var extension = System.IO.Path.GetExtension(frame);
                yield return new ImageSequence
                {
                    Name = System.IO.Path.GetFileName(entry),
                    FileName = System.IO.Path.Combine(entry, "frame-%03d" + extension)
                };
            }
        }
        
        foreach (var entry in Directory.EnumerateFiles(Path))
        {
            yield return new ImageSequence
            {
                Name = System.IO.Path.GetFileNameWithoutExtension(entry),
                FileName = entry
            };
        }
    }
}
