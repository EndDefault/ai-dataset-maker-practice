# 데이터 모델

## Translation Job

텍스트 입력 또는 이미지 영역 하나를 번역하는 작업 단위다.

```json
{
  "id": "job-001",
  "sourceType": "image",
  "status": "normalized",
  "source": {
    "language": "en",
    "text": "I didn't say it was easy."
  },
  "ocr": {
    "enabled": true,
    "engine": "paddleocr",
    "rawText": "I didn't say it was easy.",
    "correctedText": "I didn't say it was easy.",
    "confidence": 0.91,
    "reviewed": true
  },
  "image": {
    "imageId": "image-001",
    "imagePath": "data/images/page-001.png",
    "regionId": "region-001",
    "box": {
      "x": 120,
      "y": 80,
      "width": 340,
      "height": 90
    },
    "cropPath": "data/crops/page-001-region-001.png"
  },
  "translation": {
    "draft": "나는 그게 쉽다고 말하지 않았다.",
    "normalized": "쉽다고 한 적은 없어.",
    "final": "쉽다고 한 적은 없어.",
    "reviewed": false
  },
  "references": [],
  "metadata": {
    "createdAt": "",
    "updatedAt": ""
  }
}
```

## 상태값

| 상태 | 의미 |
| --- | --- |
| `created` | 작업 생성 |
| `region_created` | 이미지 영역 지정 완료 |
| `ocr_done` | OCR 추출 완료 |
| `ocr_reviewed` | OCR 결과 검수 완료 |
| `translated` | 초벌 번역 완료 |
| `normalized` | 자연스러운 한국어 정규화 완료 |
| `translation_reviewed` | 최종 번역 검수 완료 |
| `rejected` | 사용하지 않음 |

## 이미지 영역

이미지 전체를 OCR하지 않고 사용자가 번역할 영역을 직접 지정한다.

```json
{
  "id": "region-001",
  "imageId": "image-001",
  "box": {
    "x": 120,
    "y": 80,
    "width": 340,
    "height": 90
  },
  "cropPath": "data/crops/page-001-region-001.png",
  "status": "ocr_done"
}
```

## 저장 원칙

- 원본 이미지와 crop 이미지는 파일로 저장하고 JSON에는 경로를 남긴다.
- OCR 결과는 `rawText`와 `correctedText`를 분리한다.
- 번역 결과는 `draft`, `normalized`, `final`을 분리한다.
- 데이터셋 생성과 JSONL export는 MVP 범위가 아니다.
- 나중에 필요하면 사람이 검수한 번역 기록을 별도 export 기능으로 확장한다.
