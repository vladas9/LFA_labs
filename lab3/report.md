# DSL for music creation

First of all we should provide the possibility to let user define different chunks. As layers.  
Each chunk will contain it's own music definition. Chunks are needed if user wants to define overlapping music, like drums at the same time as guitar. He defines a chunk for guitar, a chunk for the drums and write music definition for each

```
//some code to 
//play music here
```

```
//some code to play 
//music there
```

Chunks are played at the same time

## Constant definitions:

Constants defined at each chunk to understand how the user wants the current chunk to be played

- `TimeSignature=a/b` - (By default 4/4) - watch video 1 from Relevant links to understand what is this. Mainly needed to draw correctly the musical sheet
- `Tempo=x` - music tempo in Ms per beat or BPM, in musical sheet as allegro, moderato, lento
- `Volume=y` - Volume of chunk. In computer definition can be expressed in LUFS or Decibels. In music sheet is defined as ppp, pp, p, mp, mf, f, ff, fff

[![](https://private-user-images.githubusercontent.com/103861986/413540474-89eec042-7290-4e74-8f71-40304321700e.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDI3OTg2MjcsIm5iZiI6MTc0Mjc5ODMyNywicGF0aCI6Ii8xMDM4NjE5ODYvNDEzNTQwNDc0LTg5ZWVjMDQyLTcyOTAtNGU3NC04ZjcxLTQwMzA0MzIxNzAwZS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwMzI0JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDMyNFQwNjM4NDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0xNmVjMTY3NDY4MjIyYmQxOGNmMGMwNmZkMDUzMDc5ZDhiMmFhYzIxNjBlZjU1NjgyNjllY2M0MTRmOWQ0OWE0JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.yQ6Kj7Vqf8MXXJ77hjXGhW69Tni_I8V3zJCHlmw1yNI)](https://private-user-images.githubusercontent.com/103861986/413540474-89eec042-7290-4e74-8f71-40304321700e.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDI3OTg2MjcsIm5iZiI6MTc0Mjc5ODMyNywicGF0aCI6Ii8xMDM4NjE5ODYvNDEzNTQwNDc0LTg5ZWVjMDQyLTcyOTAtNGU3NC04ZjcxLTQwMzA0MzIxNzAwZS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwMzI0JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDMyNFQwNjM4NDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT0xNmVjMTY3NDY4MjIyYmQxOGNmMGMwNmZkMDUzMDc5ZDhiMmFhYzIxNjBlZjU1NjgyNjllY2M0MTRmOWQ0OWE0JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.yQ6Kj7Vqf8MXXJ77hjXGhW69Tni_I8V3zJCHlmw1yNI)

## Sound definitions:

Beats are the most important measurement units to define the note duration. There are 5 main sound durations that we need to consider:

1. _Quarter note_ - 1 beat
2. _Half note_ - 2 consecutive beats
3. _Whole note_ - 4 consecutive beats
4. _Eigth note_ - 1/2 beat (2x less then a quarter)
5. _16th note_ - 1/4 beat (4x less than a quarter)

To understand better you can try to downlad a metronome and set it to 500ms. Now if you try to clap at each beat it will be a quarter of note, then just try to clap 2 times, 4 times faster/slower to understand how this works. Also check a [useful video](https://youtu.be/ZoxN0wOmw-Q?si=zk-XzM2LhwfT7fwK) to get the basics of how these notes look on the musical sheet.

We know about do re mi. But there is another notation of note value that can be used. It is by matching English alphabet letters (A-F) with them. I think we should stick with one easier to implement for all instruments, but for now don't be afraid if you see somewhere `sol` and in another place `G`. Meaning will be the same.

So now since we both know these basics let's talk about instruments

### Pause

`Pause(x)` - x defines the duration of pause expressed in amount of beats that need to be skipped (1, 2, 1/2, etc.). Called also the rest notes

### Piano

Piano has too many keys to be expressed only in 5 rows on musical sheet. This is why pianists use 2 rows to define the notes. One for the right hand (starts with Sol cleff), another for the left hand (bas key)

[![Image](https://private-user-images.githubusercontent.com/103861986/413540492-a4bbf80f-716d-4199-93cf-681132c88b2c.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDI3OTg2MjcsIm5iZiI6MTc0Mjc5ODMyNywicGF0aCI6Ii8xMDM4NjE5ODYvNDEzNTQwNDkyLWE0YmJmODBmLTcxNmQtNDE5OS05M2NmLTY4MTEzMmM4OGIyYy5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwMzI0JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDMyNFQwNjM4NDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1hMjJkZmFhMjA3NzM3NDhjNzYxMWJmM2RiNGRhYzg0Yzk2YzEyNDQxMGM3ODU5NzdlZGJhYzI3OWUyNjYzYzFhJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.690RaRNaUPhfFNX9HUzbYLfwiVnLXiLvwWh8-nWXmN4)](https://private-user-images.githubusercontent.com/103861986/413540492-a4bbf80f-716d-4199-93cf-681132c88b2c.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDI3OTg2MjcsIm5iZiI6MTc0Mjc5ODMyNywicGF0aCI6Ii8xMDM4NjE5ODYvNDEzNTQwNDkyLWE0YmJmODBmLTcxNmQtNDE5OS05M2NmLTY4MTEzMmM4OGIyYy5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwMzI0JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDMyNFQwNjM4NDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1hMjJkZmFhMjA3NzM3NDhjNzYxMWJmM2RiNGRhYzg0Yzk2YzEyNDQxMGM3ODU5NzdlZGJhYzI3OWUyNjYzYzFhJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.690RaRNaUPhfFNX9HUzbYLfwiVnLXiLvwWh8-nWXmN4)

#### Code definition

There are much more details about pianos, but I think we need to stick for the basics here and provide the user the following syntax:

```
Piano(R, do, 2/4) //right hand do half note
Piano(L, sol, 1/4) //left hand sol quarter note
Piano(L, fa, 1/4) //left hand fa quarter note
```

This will play 3 notes keys with a total duration of 4 beats or 1 entire Measure

### Guitar

As you maybe know the guitar has 6 strings with it's notation for each string expressed in letters of the English alphabet (A-F). Also for each sound on the guitar cliff there are their own notations, so we are lucky. To read from the lowest sound to the highest go from bottom row to the right, go to the beginning of the row above and repeat:

[![Image](https://private-user-images.githubusercontent.com/103861986/413540566-c84e0c2b-5cc2-44ee-9a43-25fd409ed4a8.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDI3OTg2MjcsIm5iZiI6MTc0Mjc5ODMyNywicGF0aCI6Ii8xMDM4NjE5ODYvNDEzNTQwNTY2LWM4NGUwYzJiLTVjYzItNDRlZS05YTQzLTI1ZmQ0MDllZDRhOC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwMzI0JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDMyNFQwNjM4NDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT05ZjRjYTNjMzc1NzY5ZjQzNTAyMmUxNzg2MjY1MmQ5Y2Q0MGJhZTcwY2U0MDJmYTg1NTEzYWE5MmNjMDg2MzNmJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.kGSpeNLPTJ6Q8dvVC-syuaKGy-fLJLatK5Tne6XoZwo)](https://private-user-images.githubusercontent.com/103861986/413540566-c84e0c2b-5cc2-44ee-9a43-25fd409ed4a8.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDI3OTg2MjcsIm5iZiI6MTc0Mjc5ODMyNywicGF0aCI6Ii8xMDM4NjE5ODYvNDEzNTQwNTY2LWM4NGUwYzJiLTVjYzItNDRlZS05YTQzLTI1ZmQ0MDllZDRhOC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwMzI0JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDMyNFQwNjM4NDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT05ZjRjYTNjMzc1NzY5ZjQzNTAyMmUxNzg2MjY1MmQ5Y2Q0MGJhZTcwY2U0MDJmYTg1NTEzYWE5MmNjMDg2MzNmJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.kGSpeNLPTJ6Q8dvVC-syuaKGy-fLJLatK5Tne6XoZwo)

We will need to figure out how to deal with 1st and 6th string since the sound the notation is the same, but sound is totally different  
This is how we can relate them on the sheet:

[![Image](https://private-user-images.githubusercontent.com/103861986/413540579-bd202876-df92-490d-8707-07443e34b5e1.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDI3OTg2MjcsIm5iZiI6MTc0Mjc5ODMyNywicGF0aCI6Ii8xMDM4NjE5ODYvNDEzNTQwNTc5LWJkMjAyODc2LWRmOTItNDkwZC04NzA3LTA3NDQzZTM0YjVlMS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwMzI0JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDMyNFQwNjM4NDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1mNWM3ZjJjMmU2NWM5MWFlM2JkNWU0ODUyODAwYTNmMjA0ZGFlNTIxNjU1ZmIwZjU1ZDkxZjU1ODEwM2FkYmM0JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.D1VIrG_Yc1Aqk1cJrla-VkgNZCJM5xb8j2NImYssU_4)](https://private-user-images.githubusercontent.com/103861986/413540579-bd202876-df92-490d-8707-07443e34b5e1.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDI3OTg2MjcsIm5iZiI6MTc0Mjc5ODMyNywicGF0aCI6Ii8xMDM4NjE5ODYvNDEzNTQwNTc5LWJkMjAyODc2LWRmOTItNDkwZC04NzA3LTA3NDQzZTM0YjVlMS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwMzI0JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDMyNFQwNjM4NDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1mNWM3ZjJjMmU2NWM5MWFlM2JkNWU0ODUyODAwYTNmMjA0ZGFlNTIxNjU1ZmIwZjU1ZDkxZjU1ODEwM2FkYmM0JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.D1VIrG_Yc1Aqk1cJrla-VkgNZCJM5xb8j2NImYssU_4)

Also symbols that you might see near the letters on the guitar riff can be places as they are near the notes like this. These symbols make the note slightly sharper or flatter, but it does not change the position on the musical sheet

[![](https://private-user-images.githubusercontent.com/103861986/413540602-33f9e49e-a93b-4910-9527-38c184e8c7c9.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDI3OTg2MjcsIm5iZiI6MTc0Mjc5ODMyNywicGF0aCI6Ii8xMDM4NjE5ODYvNDEzNTQwNjAyLTMzZjllNDllLWE5M2ItNDkxMC05NTI3LTM4YzE4NGU4YzdjOS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwMzI0JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDMyNFQwNjM4NDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT05MzdkNjMxMDkyYTFmYzM4NDA3NDI2YzBiODViOGUwOWI4OTRmMDgxYjBhYzA0ZmNjN2ZhY2RhMzg5ZDY4OWFjJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.RGKYp_mvQK6S1Pz4UnTmD8rAvet-okbbAL7frDcG3tE)](https://private-user-images.githubusercontent.com/103861986/413540602-33f9e49e-a93b-4910-9527-38c184e8c7c9.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDI3OTg2MjcsIm5iZiI6MTc0Mjc5ODMyNywicGF0aCI6Ii8xMDM4NjE5ODYvNDEzNTQwNjAyLTMzZjllNDllLWE5M2ItNDkxMC05NTI3LTM4YzE4NGU4YzdjOS5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjUwMzI0JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI1MDMyNFQwNjM4NDdaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT05MzdkNjMxMDkyYTFmYzM4NDA3NDI2YzBiODViOGUwOWI4OTRmMDgxYjBhYzA0ZmNjN2ZhY2RhMzg5ZDY4OWFjJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.RGKYp_mvQK6S1Pz4UnTmD8rAvet-okbbAL7frDcG3tE)

#### Code definition

```
guitar(G, A, 1/4) //base string, accord on cliff, duration
```

## Loops

We can have 2 main use cases for loops. Loops for changing the notes at each interation, another for just repeating the same music certain amount of times

```
for(note = re; note < si; note+=1){
  piano(R, note, 1/4)
}
for(i = 0; i < 10; note+=1){
  piano(R, re, 1/4)
} 
```

## Sync chunks

Also in order to define multiple notes played at the same time person can define in a chunk

```
sync{
  piano(R, note, 1/4)
  piano(R, re, 1/4)
}
```

Both notes will be played simultaneously

---

Conclusion

This DSL provides a structured yet flexible way for users to define musical pieces. By breaking the composition into chunks, each with its own constants like time signature, tempo, and volume, it becomes easier to layer and synchronize different instruments such as piano and guitar. The inclusion of clear syntax for note durations, pauses, and loops—along with support for simultaneous playback through sync blocks—ensures that users have the necessary tools to craft intricate musical arrangements. Overall, this DSL serves as a solid foundation for both beginners and advanced musicians to experiment with and refine their creative process.

---
# Relevant links:

1. [Understanding basic rythm video explanation](https://youtu.be/ZoxN0wOmw-Q?si=zk-XzM2LhwfT7fwK)
2. [How to read music sheets(guitar)](https://youtu.be/8bzAjQ4PxyA?si=obaMmeKy7t1q0d7w)
