using Bonsai;
using System;
using System.ComponentModel;
using System.Linq;
using System.Reactive.Linq;
using System.Drawing;
using System.Globalization;

[Combinator]
[Description("Convert a text based representation of color into a color object.")]
[WorkflowElementCategory(ElementCategory.Transform)]
public class ParseColor
{
    readonly ColorConverter converter = new ColorConverter();

    public IObservable<Color> Process(IObservable<string> source)
    {
        return source.Select(value => (Color)converter.ConvertFrom(null, CultureInfo.InvariantCulture, value));
    }
}
