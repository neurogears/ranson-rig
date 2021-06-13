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

    public IObservable<int> Process(IObservable<FrameEvent> source)
    {
        return Observable.Defer(() =>
        {
            var state = 0;
            var random = new Random(Seed);
            var distribution = new Geometric(P, random);
            var next = distribution.Sample();
            return source.Select(value =>
            {
                if (next-- <= 0)
                {
                    next = distribution.Sample();
                    state = 1 - state;
                }

                return state;
            });
        });
    }
}
