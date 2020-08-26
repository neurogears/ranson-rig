using Bonsai;
using System;
using System.ComponentModel;
using System.Reactive.Linq;
using Bonsai.Shaders;

[Combinator]
[Description("Declares a texture type for initialization.")]
[WorkflowElementCategory(ElementCategory.Source)]
public class TextureSource
{
    public IObservable<Texture> Process()
    {
        return Observable.Empty<Texture>();
    }
}
