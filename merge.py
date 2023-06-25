from model import model
from spliting import split


def make_segments(text):
    return [
        {
            'text': segment,
            'scores': {
                predict['label']: predict['score']
                for predict in model(segment, top_k=None)
            }
        }
        for segment in split(text)
    ]


def merge_segments(segment1, segment2):
    segment = segment1['text'] + ' ' + segment2['text']
    return {
        'text': segment,
        'scores': {
            predict['label']: predict['score']
            for predict in model(segment, top_k=None)
        }
    }


def merge_by_sim(segments, bottom_threshold, top_threshold):
    i = 0
    while i != len(segments) - 1:
        conf_1 = max(segments[i]['scores'].values())
        conf_2 = max(segments[i + 1]['scores'].values())

        try:
            merged = merge_segments(segments[i], segments[i + 1])
        except RuntimeError:
            i += 1
            continue

        conf_m = max(merged['scores'].values())
        if (
            (conf_m > top_threshold) and
            (conf_1 < bottom_threshold or conf_2 < bottom_threshold)
        ):
            segments[i] = merged
            segments.pop(i + 1)
        else:
            i += 1


def merge_by_same(segments):
    i = 0
    while i != len(segments) - 1:
        merged = merge_segments(segments[i], segments[i + 1])

        conf = (
            max(segments[i]['scores'], key=segments[i]['scores'].get) ==
            max(segments[i + 1]['scores'], key=segments[i + 1]['scores'].get)
        )
        if conf:
            segments[i] = merged
            segments.pop(i + 1)
        else:
            i += 1


def set_low_as(segments, as_, threshold):
    for i in range(len(segments)):
        cls = max(segments[i]['scores'], key=segments[i]['scores'].get)
        if segments[i]['scores'][cls] < threshold:
            segments[i]['scores'][as_] = threshold + 0.1


def segmentize_and_merge(text):
    segments = make_segments(text)

    merge_by_sim(segments, 0.93, 0.96)
    merge_by_same(segments)

    set_low_as(segments, 'notes', 0.56)

    result = [
        [
            segment['text'],
            max(segment['scores'], key=segment['scores'].get)
        ]
        for segment in segments
    ]

    return result
