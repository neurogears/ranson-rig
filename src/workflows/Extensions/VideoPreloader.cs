using Bonsai;
using System.ComponentModel;
using System.Collections.Generic;
using System;
using System.Reactive.Linq;
using Bonsai.Shaders;
using System.Linq;
using Bonsai.Shaders.Configuration;
using System.IO;

[Combinator]
[Description("Preloads a specified collection of videos.")]
[WorkflowElementCategory(ElementCategory.Combinator)]
public class VideoPreloader : Combinator<IList<string>, IDisposable>
{
    UpdateFrame update = new UpdateFrame();

    public override IObservable<IDisposable> Process(IObservable<IList<string>> source)
    {
        return from list in source
               from update in update.Generate().Take(1)
               let resources = list.Select(path =>
               {
                   if (Directory.Exists(path))
                   {
                       var frame = Directory.EnumerateFiles(path).First();
                       var extension = Path.GetExtension(frame);
                       return new ImageSequence
                       {
                           Name = Path.GetFileName(path),
                           FileName = Path.Combine(path, "frame-%03d" + extension)
                       };
                   }
                   else return new ImageSequence
                   {
                       Name = Path.GetFileNameWithoutExtension(path),
                       FileName = path
                   };
               })
               let window = (ShaderWindow)update.Sender
               select window.ResourceManager.Load(resources);
    }
}
