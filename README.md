# Llama o1-preview experiment

Эксперимент в котором я попытался собрать аналог `o1-preview` используя при этом две `llama3.1:8b`.

При этом через ollama использовалось две модели:

- первая работает в режиме Chain of Thoughts (CoT модель), её задача сгенерировать цепочку размышлений
- вторая (Basic модель) принимает в контекст цепочку размышлений и вопрос пользователя и пытается дать ответ с учётом
  размышлений сделанных CoT моделью

Запись стрима доступна
на: [Дзен](https://dzen.ru/video/watch/66e63069d60c1010815386ad), [ВК](https://vk.com/evilfreelancer?z=video-216892577_456239091%2Fvideos-216892577%2Fpl_-216892577_-2)
и [YouTube](https://www.youtube.com/watch?v=0upnhlTVB4w).

## Как это работает

Логика работы приложения очень простая:

![Схема приложения](./assets/example.jpg)

1) сначала мы считываем запрос пользователя;
2) запрос пользователя вместе с системным промтом из cot-promtp.txt отправляется в CoT модель, после чего получаем
   ответ;
3) указанный ответ вместе с системным промтом из basic-prompt.txt помещается в память чата базовой модели;
4) выполняет инференс на базовой модели и ответ возвращается пользователю;
5) GOTO 1).

## Что было сделано

По ходу стрима было реализовано и оптимизировано два системных промта, первый называется
[cot-prompt.txt](https://github.com/EvilFreelancer/llama-o1-preview/blob/main/cot-prompt.txt) и передаётся на вход модели
имитирующей логические размышления (Chain of Thoughts или просто CoT) в нём мы просим модель строить логические цепочки
о вопросе пользователя, второй называется
[basic-prompt.txt](https://github.com/EvilFreelancer/llama-o1-preview/blob/main/basic-prompt.txt), в нём мы просим модель
используя логические размышления из полученные на предыдущем шаге дать ответ на вопрос пользователя.

Помимо этого была реализована специальная [память чата](https://github.com/EvilFreelancer/llama-o1-preview/blob/main/chat_history.py), она настроена таким образом, чтобы
в истории был только системный промт, цепочка размышлений и вопрос пользователя.

## Ссылки

Почитать подробнее про reasoning
[тут](https://platform.openai.com/docs/guides/reasoning?reasoning-prompt-examples=research), а тематически похожие
публикации на arxiv [тут](https://arxiv.org/abs/2401.08967), [тут](https://arxiv.org/abs/2402.05808) и
[тут](https://arxiv.org/abs/2407.21787) (увидел ссылки на канале [DealerAI](https://t.me/dealerAI)).
