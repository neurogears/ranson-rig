using Bonsai;
using System;
using System.ComponentModel;
using System.Linq;
using System.Reactive.Linq;
using Bonsai.Shaders;
using MathNet.Numerics.Distributions;

[Combinator]
[Description("Generates a pseudo-random sync sequence for photodiode alignment.")]
[WorkflowElementCategory(ElementCategory.Transform)]
public class SyncSequence
{
    public int Seed { get; set; }

    public double P { get; set; }

    public int Offset { get; set; }

    public IObservable<int> Process<TSource>(IObservable<TSource> source)
    {
        return Observable.Defer(() =>
        {
            var next = 0;
            var state = 0;
            var offset = Offset;
            var random = new Random(Seed);
            var distribution = new Geometric(P, random);
            return source.Select(value =>
            {
                if (next-- <= 0)
                {
                    next = distribution.Sample() + offset;
                    state = 1 - state;
                }

                return state;
            });
        });
    }
}
