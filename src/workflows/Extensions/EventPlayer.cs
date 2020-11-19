using Bonsai;
using System;
using System.ComponentModel;
using System.Linq;
using System.Reactive.Linq;
using Bonsai.Shaders;
using System.Reactive;

[Combinator]
[Description("Replays a timestamped event sequence using frame time.")]
[WorkflowElementCategory(ElementCategory.Combinator)]
public class EventPlayer
{
    readonly UpdateFrame updateFrame = new UpdateFrame();

    public IObservable<TData> Process<TData>(IObservable<Tuple<double, TData>[]> source)
    {
        return source.SelectMany(events => Observable.Create<TData>(observer =>
        {
            var index = 0;
            var elapsedTime = 0.0;
            var frameObserver = Observer.Create<FrameEvent>(
                evt =>
                {
                    elapsedTime += evt.TimeStep.ElapsedTime;
                    while (index < events.Length &&
                           Math.Abs(elapsedTime - events[index].Item1) < 1e-10)
                    {
                        observer.OnNext(events[index].Item2);
                        index++;
                    }
                },
                observer.OnError,
                observer.OnCompleted);
            return updateFrame.Generate().SubscribeSafe(frameObserver);
        }));
    }
}
