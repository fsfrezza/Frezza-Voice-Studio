# Locutor DBZ — perfil nativo de voz

## Objetivo
O Frezza Voice Studio usa o perfil **Locutor DBZ** nos fluxos existentes do VoiceStudio v0.5.6:

- **Texto → voz:** selecione o perfil em Generate, escreva o texto e sintetize.
- **Áudio → mesma fala com voz do locutor:** use Convert, escolha o perfil e envie o áudio original. O backend transcreve o áudio com ASR e ressintetiza por TTS usando a voz clonada, sem substituir literalmente o timbre do áudio original amostra a amostra. Por isso, a prosódia, pausas, sotaque e duração podem variar. Há uma opção existente de ajuste aproximado de duração.

## Instalação do perfil no aplicativo
Inicie o backend do VoiceStudio/Frezza Voice Studio e, no computador que possui os arquivos do usuário:

```powershell
python scripts/install_locutor_profile.py --audio "sample.mp3" --image "locutor dbz.jpg"
```

O utilitário normaliza o conteúdo para WAV mono PCM 24 kHz usando FFmpeg e chama a API **nativa** `POST /profiles`, com o retrato e a voz. A extensão do arquivo original não é presumida como codec — o `sample.mp3` fornecido tem, na realidade, conteúdo WebM/Opus. O registro fica persistido no banco local do aplicativo, com um ID de perfil. Para melhores resultados, pode-se adicionar `--ref-text "transcrição exata da amostra"` (a transcrição deve corresponder exatamente ao trecho usado).

## Considerações de qualidade
A amostra original tem cerca de 59 segundos. Quanto menos música, reverberação ou efeitos misturados ao locutor, melhor tende a ser a semelhança. O uso de trechos selecionados de fala limpa pode resultar em desempenho mais consistente do que usar uma gravação longa sem tratamento. A clonagem exata não é garantida e depende do motor TTS e da disponibilidade dos pesos. Conversão requer também ASR instalado. Usar vozes apenas quando tiver direitos para isso.

## Estado
O script de instalação do perfil está implementado. A referência **não está embutida no repositório**: precisa ser adicionada pelo usuário usando o comando acima. Não foi executado um teste de síntese/voz convertida neste repositório; a importação do upstream e o build seguem pendentes de execução no Actions.
